import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
import numpy as np
import cv2
import sys
import os

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Modül yolunu ayarlama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud, schemas
from database.config import get_db
from ai_module.face_recognition import FaceRecognitionSystem

router = APIRouter(
    prefix="/face-recognition",
    tags=["face-recognition"],
    responses={404: {"description": "Not found"}},
)

# Yüz tanıma sistemi örneği
face_recognition_system = None

def init_face_recognition_system():
    global face_recognition_system
    if face_recognition_system is None:
        face_recognition_system = FaceRecognitionSystem()
    return face_recognition_system

@router.post("/register-face/{user_id}")
async def register_face(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Kullanıcının referans fotoğrafını kaydet"""
    try:
        # Kullanıcıyı kontrol et
        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

        # Dosyayı oku ve numpy dizisine dönüştür
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # BGR'dan RGB'ye dönüştür
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Yüz tanıma sistemini başlat
        face_system = init_face_recognition_system()

        # Yüzleri tespit et
        faces = face_system.detect_faces(image_rgb)
        if not faces:
            raise HTTPException(status_code=400, detail="Fotoğrafta yüz bulunamadı")

        # En büyük yüzü al
        face = max(faces, key=lambda x: x['box'][2] * x['box'][3])
        if face['confidence'] < 0.98:
            raise HTTPException(status_code=400, detail="Yüz tespit güveni düşük")

        # Yüz bölgesini kes
        x, y, w, h = face['box']
        # Sınırları kontrol et
        x = max(0, x)
        y = max(0, y)
        w = min(w, image_rgb.shape[1] - x)
        h = min(h, image_rgb.shape[0] - y)
        
        face_image = image_rgb[y:y+h, x:x+w]
        
        # Yüz görüntüsünü yeniden boyutlandır
        face_image = cv2.resize(face_image, (224, 224))

        # Referans fotoğrafı olarak kaydet
        save_path = os.path.join('data', 'test_images', f"{db_user.name}_{user_id}.jpg")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        cv2.imwrite(save_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))

        return {
            "message": "Referans fotoğrafı başarıyla kaydedildi",
            "confidence": face['confidence']
        }

    except Exception as e:
        logger.error(f"Yüz işleme hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recognize")
async def recognize_face(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    min_confidence: float = 0.65
):
    """Gönderilen fotoğraftaki yüzü tanı ve yoklama kaydı oluştur"""
    try:
        # Yüz tanıma sistemini başlat
        face_system = init_face_recognition_system()

        # Dosyayı oku ve numpy dizisine dönüştür
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Yüzleri tanı
        recognized_faces = face_system.process_image(image)
        if not recognized_faces:
            return {"recognized_people": [], "message": "Yüz tespit edilemedi"}

        # Sonuçları formatla ve yoklama kayıtları oluştur
        recognized_people = []
        for face in recognized_faces:
            # Güven skoru kontrolü
            if face["confidence"] < min_confidence:
                logger.warning(f"Düşük güven skoru ({face['confidence']:.2f}) - {face['name']}")
                continue

            person_info = {
                "name": face["name"],
                "confidence": face["confidence"],
                "attendance_status": "not_recorded"
            }
            
            try:
                # Kullanıcıyı bul
                db_user = crud.get_user_by_name(db, name=face["name"])
                if db_user:
                    # Bugünkü yoklamaları kontrol et
                    today = datetime.utcnow()
                    daily_attendances = crud.get_daily_attendances(db, today)
                    user_attended = any(att.user_id == db_user.id for att in daily_attendances)
                    
                    if user_attended:
                        person_info["attendance_status"] = "already_attended"
                        logger.info(f"{face['name']} bugün zaten yoklamaya katılmış")
                    else:
                        # Yeni yoklama kaydı oluştur
                        attendance = schemas.AttendanceCreate(
                            user_id=db_user.id,
                            check_in_time=today,
                            confidence_score=face["confidence"],
                            status="present"
                        )
                        db_attendance = crud.create_attendance(db, attendance)
                        person_info["attendance_id"] = db_attendance.id
                        person_info["attendance_status"] = "recorded"
            except Exception as e:
                logger.warning(f"Yoklama kaydı oluşturulamadı: {e}")
                person_info["attendance_status"] = "error"
                
            recognized_people.append(person_info)

        # Sonuç mesajını hazırla
        if not recognized_people:
            message = "Yeterli güven skoruna sahip yüz bulunamadı"
        else:
            new_records = sum(1 for p in recognized_people if p["attendance_status"] == "recorded")
            already_attended = sum(1 for p in recognized_people if p["attendance_status"] == "already_attended")
            message = f"{len(recognized_people)} kişi tanındı"
            if already_attended > 0:
                message += f" ({already_attended} kişi bugün zaten yoklamaya katılmış)"

        return {
            "recognized_people": recognized_people,
            "message": message,
            "min_confidence": min_confidence
        }

    except Exception as e:
        logger.error(f"Yüz tanıma hatası: {e}")
        return {"recognized_people": [], "error": str(e)}

@router.post("/recognize-video")
async def recognize_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    min_confidence: float = 0.60,  # Güven skorunu düşürdük
    frame_interval: int = 1,       # Her frame'i işle
    max_frames: int = 30,          # Daha fazla frame işle
    timeout_seconds: int = 10
):
    try:
        temp_file = f"temp_video_{datetime.utcnow().timestamp()}.mp4"
        
        with open(temp_file, "wb") as buffer:
            buffer.write(await file.read())
        
        face_system = init_face_recognition_system()
        cap = cv2.VideoCapture(temp_file)
        if not cap.isOpened():
            return {"recognized_people": [], "message": "Video açılamadı", "should_stop": True}
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        processed_frames = 0
        frame_count = 0
        start_time = datetime.utcnow()
        recognized_faces = {}
        found_face = False  # Yüz bulunduğunda işlemi durdurmak için flag
        
        actual_interval = max(1, min(frame_interval, total_frames // max_frames))
        logger.info(f"Frame atlama aralığı: {actual_interval}")
        
        while frame_count < total_frames and not found_face:  # found_face kontrolü ekledik
            if (datetime.utcnow() - start_time).seconds > timeout_seconds:
                logger.warning("Video işleme zaman aşımına uğradı")
                break
                
            if processed_frames >= max_frames:
                logger.info("Maksimum frame sayısına ulaşıldı")
                break
            
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            if frame_count % actual_interval != 0:
                continue
                
            processed_frames += 1
            logger.info(f"Frame işleniyor: {processed_frames}/{max_frames} (Video frame: {frame_count}/{total_frames})")
            
            faces = face_system.process_image(frame)
            if faces:
                for face in faces:
                    name = face["name"]
                    confidence = face["confidence"]
                    if confidence >= min_confidence:  # Güven skoru yeterliyse
                        recognized_faces[name] = confidence
                        logger.info(f"Yüz tanındı: {name} (Güven: {confidence:.2f})")
                        found_face = True  # Yüz bulundu, döngüyü sonlandır
                        break
                
                if found_face:  # İç döngüden çıktıktan sonra da kontrol et
                    break
        
        cap.release()
        
        if not recognized_faces:
            return {
                "recognized_people": [],
                "message": "Videoda yüz tespit edilemedi",
                "processed_frames": processed_frames,
                "should_stop": True
            }

        recognized_people = []
        for name, confidence in recognized_faces.items():
            person_info = {
                "name": name,
                "confidence": confidence,
                "attendance_status": "not_recorded"
            }
            
            try:
                db_user = crud.get_user_by_name(db, name=name)
                if db_user:
                    today = datetime.utcnow()
                    daily_attendances = crud.get_daily_attendances(db, today)
                    user_attended = any(att.user_id == db_user.id for att in daily_attendances)
                    
                    if user_attended:
                        person_info["attendance_status"] = "already_attended"
                        logger.info(f"{name} bugün zaten yoklamaya katılmış")
                    else:
                        attendance = schemas.AttendanceCreate(
                            user_id=db_user.id,
                            check_in_time=today,
                            confidence_score=confidence,
                            status="present"
                        )
                        db_attendance = crud.create_attendance(db, attendance)
                        person_info["attendance_id"] = db_attendance.id
                        person_info["attendance_status"] = "recorded"
            except Exception as e:
                logger.warning(f"Yoklama kaydı oluşturulamadı: {e}")
                person_info["attendance_status"] = "error"
                
            recognized_people.append(person_info)

        if not recognized_people:
            message = "Yeterli güven skoruna sahip yüz bulunamadı"
        else:
            new_records = sum(1 for p in recognized_people if p["attendance_status"] == "recorded")
            already_attended = sum(1 for p in recognized_people if p["attendance_status"] == "already_attended")
            message = f"{len(recognized_people)} kişi tanındı"
            if already_attended > 0:
                message += f" ({already_attended} kişi bugün zaten yoklamaya katılmış)"

        return {
            "recognized_people": recognized_people,
            "message": message,
            "min_confidence": min_confidence,
            "processed_frames": processed_frames,
            "total_frames": total_frames,
            "should_stop": True
        }

    except Exception as e:
        logger.error(f"Video işleme hatası: {e}")
        return {
            "recognized_people": [], 
            "error": str(e),
            "should_stop": True  # Hata durumunda da videoyu durdur
        }
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file) 