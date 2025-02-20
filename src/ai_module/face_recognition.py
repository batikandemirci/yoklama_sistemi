import cv2
import numpy as np
from pathlib import Path
import logging
from tqdm import tqdm
from deepface import DeepFace
from mtcnn import MTCNN
import tensorflow as tf

# GPU bellek kullanımını sınırla
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Sabit değişkenler
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
TEST_IMAGES_DIR = DATA_DIR / 'test_images'
TEST_VIDEOS_DIR = DATA_DIR / 'test_videos'
FACE_EMBEDDINGS_DIR = DATA_DIR / 'face_embeddings'
MODELS_DIR = DATA_DIR / 'models'

class FaceRecognitionSystem:
    def __init__(self):
        """Yüz tanıma sistemini başlat"""
        self.detector = MTCNN(min_face_size=60)
        self.model_name = "Facenet512"
        self.distance_metric = "cosine"
        self.threshold = 0.65  # Threshold değerini daha da artırdık
        
    def detect_faces(self, image):
        """Görüntüdeki yüzleri tespit et"""
        try:
            # BGR'dan RGB'ye dönüştür
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Yüzleri tespit et
            faces = self.detector.detect_faces(image)
            
            # Yüzleri güven skoruna göre sırala
            faces = sorted(faces, key=lambda x: x['confidence'], reverse=True)
            
            return faces
            
        except Exception as e:
            logger.error(f"Yüz tespiti hatası: {e}")
            return []
    
    def verify_face(self, face_image, reference_image):
        """İki yüz görüntüsünü karşılaştır"""
        try:
            # Görüntüleri normalize et
            face_image = cv2.resize(face_image, (224, 224))
            
            result = DeepFace.verify(
                face_image,
                reference_image,
                model_name=self.model_name,
                distance_metric=self.distance_metric,
                enforce_detection=False,
                detector_backend='skip'
            )
            return result
            
        except Exception as e:
            logger.error(f"Yüz doğrulama hatası: {e}")
            return None
    
    def find_best_match(self, face_image):
        """Verilen yüz görüntüsü için en iyi eşleşmeyi bul"""
        try:
            matches = []
            
            # Her referans fotoğrafı ile karşılaştır
            for img_path in TEST_IMAGES_DIR.glob("*.jpg"):
                person_name = img_path.stem.split('_')[0]
                
                try:
                    result = self.verify_face(face_image, str(img_path))
                    if result:
                        matches.append((person_name, result["distance"]))
                except:
                    continue
            
            if not matches:
                return None
                
            # En iyi eşleşmeyi bul
            best_match = min(matches, key=lambda x: x[1])
            person_name, score = best_match
            
            # Threshold kontrolü
            if score > self.threshold:
                logger.info(f"Eşleşme bulundu ama threshold altında: {person_name} ({1-score:.2f})")
                return None
                
            return person_name, 1 - score  # Skoru 0-1 aralığına normalize et
            
        except Exception as e:
            logger.error(f"Eşleşme hatası: {e}")
            return None
    
    def process_image(self, image):
        """Görüntüdeki yüzleri tanı"""
        try:
            # BGR'dan RGB'ye dönüştür
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Yüzleri tespit et
            faces = self.detect_faces(image_rgb)
            if not faces:
                return []
            
            recognized_people = []
            
            # Her yüz için
            for face in faces:
                if face['confidence'] < 0.85:  # Güven skorunu biraz daha düşürdük
                    continue
                    
                try:
                    # Yüz bölgesini kes
                    x, y, w, h = face['box']
                    # Sınırları kontrol et ve biraz genişlet
                    margin = int(min(w, h) * 0.1)  # %10 margin
                    x = max(0, x - margin)
                    y = max(0, y - margin)
                    w = min(w + 2*margin, image_rgb.shape[1] - x)
                    h = min(h + 2*margin, image_rgb.shape[0] - y)
                    
                    face_image = image_rgb[y:y+h, x:x+w]
                    
                    # En iyi eşleşmeyi bul
                    result = self.find_best_match(face_image)
                    if result:
                        person_name, confidence = result
                        recognized_people.append({
                            "name": person_name,
                            "confidence": confidence
                        })
                except Exception as e:
                    logger.error(f"Yüz işleme hatası: {str(e)}")
                    continue
            
            return recognized_people
            
        except Exception as e:
            logger.error(f"Görüntü işleme hatası: {e}")
            return []
    
    def process_video(self, video_path):
        """Video üzerinde yüz tanıma işlemi gerçekleştir"""
        try:
            video_name = Path(video_path).name
            logger.info(f"Video işleniyor: {video_name}")
            
            # Videoyu aç
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                logger.error("Video açılamadı")
                return False
            
            frame_count = 0
            recognized_persons = {}  # Kişi -> [en yüksek güven skoru, tespit sayısı]
            total_frames_processed = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                
                # Her 2 frame'de bir işle
                if frame_count % 2 != 0:
                    continue
                    
                total_frames_processed += 1
                
                # Frame'i yeniden boyutlandır
                height, width = frame.shape[:2]
                max_dimension = 800
                if max(height, width) > max_dimension:
                    scale = max_dimension / max(height, width)
                    frame = cv2.resize(frame, None, fx=scale, fy=scale)
                
                # BGR'dan RGB'ye dönüştür
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Yüzleri tespit et
                faces = self.detect_faces(frame_rgb)
                
                # Her yüz için
                for face in faces:
                    # Confidence kontrolü - daha esnek
                    if face['confidence'] < 0.80:  # Yüz tespiti için eşiği düşürdük
                        continue
                        
                    try:
                        # Yüz bölgesini kes
                        x, y, w, h = face['box']
                        # Sınırları kontrol et ve margin ekle
                        margin = int(min(w, h) * 0.2)  # %20 margin
                        x = max(0, x - margin)
                        y = max(0, y - margin)
                        w = min(w + 2*margin, frame_rgb.shape[1] - x)
                        h = min(h + 2*margin, frame_rgb.shape[0] - y)
                        
                        face_image = frame_rgb[y:y+h, x:x+w]
                        
                        # Yüz görüntüsünü yeniden boyutlandır
                        face_image = cv2.resize(face_image, (224, 224))
                        
                        # Yüzü tanı
                        result = self.process_image(face_image)
                        if result:
                            for person in result:
                                name = person["name"]
                                confidence = person["confidence"]
                                
                                if name not in recognized_persons:
                                    recognized_persons[name] = [confidence, 1]
                                else:
                                    # En yüksek güven skorunu ve tespit sayısını güncelle
                                    old_score, count = recognized_persons[name]
                                    new_score = max(old_score, confidence)  # En yüksek skoru tut
                                    recognized_persons[name] = [new_score, count + 1]
                                    
                                logger.info(f"Frame {frame_count}: {name} tespit edildi (Güven: {confidence:.2f})")
                    except Exception as e:
                        logger.error(f"Yüz işleme hatası: {e}")
                        continue
            
            cap.release()
            
            # Sonuçları filtrele
            filtered_persons = {}
            min_detections = max(2, total_frames_processed * 0.05)  # En az 2 kez veya %5'inde tespit edilmeli
            
            for person, (score, count) in recognized_persons.items():
                if count >= min_detections and score >= 0.45:  # Minimum güven skorunu düşürdük
                    filtered_persons[person] = score
                    logger.info(f"{person}: {count} kez tespit edildi, en yüksek güven skoru: {score:.2f}")
            
            # Sonuçları sırala ve raporla
            sorted_persons = sorted(filtered_persons.items(), key=lambda x: x[1], reverse=True)
            
            logger.info(f"\n{'='*50}")
            logger.info(f"Video Analiz Sonucu: {video_name}")
            logger.info(f"İşlenen frame sayısı: {total_frames_processed}")
            
            for person, score in sorted_persons:
                count = recognized_persons[person][1]
                detection_rate = (count / total_frames_processed) * 100
                logger.info(f"Kişi: {person}")
                logger.info(f"  - En yüksek güven skoru: {score:.2f}")
                logger.info(f"  - Tespit oranı: {detection_rate:.1f}%")
            
            logger.info(f"{'='*50}\n")
            
            return set(filtered_persons.keys())
            
        except Exception as e:
            logger.error(f"Video işleme hatası: {e}")
            return set()

def test_recognition_system():
    """Yüz tanıma sistemini test et"""
    try:
        # Sistemi başlat
        system = FaceRecognitionSystem()
        
        # Test videolarını işle
        logger.info("Test videoları işleniyor...")
        
        # Tek kişilik videoları test et
        for video_path in TEST_VIDEOS_DIR.glob("single_person_*.mp4"):
            recognized = system.process_video(video_path)
            logger.info(f"{video_path.name}: {', '.join(recognized)}")
        
        # Çoklu kişi videolarını test et
        for video_path in TEST_VIDEOS_DIR.glob("multi_person_*.mp4"):
            recognized = system.process_video(video_path)
            logger.info(f"{video_path.name}: {', '.join(recognized)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Test hatası: {e}")
        return False

if __name__ == "__main__":
    test_recognition_system() 