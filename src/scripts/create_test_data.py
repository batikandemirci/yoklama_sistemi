import sys
import os
from pathlib import Path
import random
from datetime import datetime, timedelta

# Modül yolunu ayarlama
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import crud, models, schemas
from database.config import SessionLocal, engine
from ai_module.create_test_videos import create_test_videos
from ai_module.face_recognition import FaceRecognitionSystem

# Test kullanıcıları
TEST_USERS = [
    {
        "name": "Johnny",
        "surname": "Depp",
        "email": "johnny.depp@test.com",
        "role": "student"
    },
    {
        "name": "Brad",
        "surname": "Pitt",
        "email": "brad.pitt@test.com",
        "role": "student"
    },
    {
        "name": "Leonardo",
        "surname": "DiCaprio",
        "email": "leonardo.dicaprio@test.com",
        "role": "student"
    },
    {
        "name": "Angelina",
        "surname": "Jolie",
        "email": "angelina.jolie@test.com",
        "role": "teacher"
    },
    {
        "name": "Scarlett",
        "surname": "Johansson",
        "email": "scarlett.johansson@test.com",
        "role": "admin"
    }
]

def create_test_users():
    """Test kullanıcılarını oluştur"""
    print("\nTest kullanıcıları oluşturuluyor...")
    db = SessionLocal()
    created_users = []

    try:
        for user_data in TEST_USERS:
            # Kullanıcı zaten var mı kontrol et
            existing_user = crud.get_user_by_email(db, user_data["email"])
            if existing_user:
                print(f"Kullanıcı zaten mevcut: {user_data['name']} {user_data['surname']}")
                created_users.append(existing_user)
                continue

            # Yeni kullanıcı oluştur
            user = schemas.UserCreate(**user_data)
            db_user = crud.create_user(db, user)
            created_users.append(db_user)
            print(f"Kullanıcı oluşturuldu: {user_data['name']} {user_data['surname']}")

    except Exception as e:
        print(f"Kullanıcı oluşturma hatası: {e}")
    finally:
        db.close()

    return created_users

def create_test_face_features():
    """Test yüz özelliklerini oluştur"""
    print("\nTest yüz özellikleri oluşturuluyor...")
    db = SessionLocal()

    try:
        # Yüz tanıma sistemini başlat
        face_system = FaceRecognitionSystem()
        
        # Test videolarını oluştur
        create_test_videos()

        # Her kullanıcı için
        users = crud.get_users(db)
        for user in users:
            # Yüz özellikleri zaten var mı kontrol et
            existing_features = crud.get_face_features(db, user.id)
            if existing_features:
                print(f"Yüz özellikleri zaten mevcut: {user.name} {user.surname}")
                continue

            # Test görüntülerinden yüz özelliklerini çıkar
            # Test görüntüleri klasörünün tam yolu
            test_images_dir = Path(r"D:\Projects\yoklama_proje_2\data\test_images")
            # Dosya adları: örneğin "johnny_depp (1).jpg"
            pattern = f"{user.name.lower()}_{user.surname.lower()} (*.jpg"
            # Not: Yukarıdaki desen, "johnny_depp (1).jpg", "johnny_depp (2).jpg", vb. dosyaları eşleyecektir.
            test_images = list(test_images_dir.glob(f"{user.name.lower()}_{user.surname.lower()} (*).jpg"))
            if not test_images:
                print(f"Test görüntüsü bulunamadı: {user.name} {user.surname}")
                continue

            # İlk fotoğrafı kullan
            test_image_path = test_images[0]

            # Yüz özelliklerini oluştur (gerçek sistemde embedding face_system'den elde edilecek)
            face_features = schemas.FaceFeaturesCreate(
                user_id=user.id,
                embedding=b"test_embedding",
                confidence_score=0.95
            )
            crud.create_face_features(db, face_features)
            print(f"Yüz özellikleri oluşturuldu: {user.name} {user.surname}")

    except Exception as e:
        print(f"Yüz özellikleri oluşturma hatası: {e}")
    finally:
        db.close()

def create_test_attendances():
    """Test yoklama kayıtlarını oluştur"""
    print("\nTest yoklama kayıtları oluşturuluyor...")
    db = SessionLocal()

    try:
        # Son 7 gün için yoklama kayıtları oluştur
        users = crud.get_users(db)
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            
            for user in users:
                # Rastgele yoklama durumu
                status = random.choice(["present", "late", "absent"])
                
                # Giriş zamanı (08:00 - 09:00 arası)
                check_in = date.replace(
                    hour=random.randint(8, 9),
                    minute=random.randint(0, 59),
                    second=0,
                    microsecond=0
                )
                
                # Çıkış zamanı (15:00 - 16:00 arası)
                check_out = date.replace(
                    hour=random.randint(15, 16),
                    minute=random.randint(0, 59),
                    second=0,
                    microsecond=0
                ) if status != "absent" else None

                # Yoklama kaydı oluştur
                attendance = schemas.AttendanceCreate(
                    user_id=user.id,
                    check_in_time=check_in,
                    confidence_score=random.uniform(0.85, 0.99),
                    status=status
                )
                crud.create_attendance(db, attendance)

            print(f"Yoklama kayıtları oluşturuldu: {date.date()}")

    except Exception as e:
        print(f"Yoklama kayıtları oluşturma hatası: {e}")
    finally:
        db.close()

def main():
    """Test verilerini oluştur"""
    print("Test verileri oluşturuluyor...")
    
    # Veritabanı tablolarını oluştur
    models.Base.metadata.create_all(bind=engine)
    
    # Test verilerini oluştur
    users = create_test_users()
    create_test_face_features()
    create_test_attendances()
    
    print("\nTest verileri başarıyla oluşturuldu!")

if __name__ == "__main__":
    main()
