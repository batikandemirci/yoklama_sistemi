import sys
import os
from pathlib import Path

# Modül yolunu ayarlama
sys.path.append(str(Path(__file__).parent.parent))

from database import crud, schemas
from database.config import SessionLocal

def create_test_users():
    """Test için örnek kullanıcılar oluştur"""
    # Test kullanıcıları
    test_users = [
        {
            "name": "angelina",
            "surname": "jolie",
            "email": "angelina@test.com",
            "role": "student"
        },
        {
            "name": "brad",
            "surname": "pitt",
            "email": "brad@test.com",
            "role": "student"
        },
        {
            "name": "leonardo",
            "surname": "dicaprio",
            "email": "leo@test.com",
            "role": "student"
        },
        {
            "name": "scarlett",
            "surname": "johansson",
            "email": "scarlett@test.com",
            "role": "student"
        },
        # Yeni kullanıcılar
        {
            "name": "hugh",
            "surname": "jackman",
            "email": "hugh@test.com",
            "role": "student"
        },
        {
            "name": "robert",
            "surname": "downey",
            "email": "robert@test.com",
            "role": "student"
        },
        {
            "name": "johnny",
            "surname": "depp",
            "email": "johnny@test.com",
            "role": "student"
        },
        {
            "name": "megan",
            "surname": "fox",
            "email": "megan@test.com",
            "role": "student"
        }
    ]
    
    # Veritabanı bağlantısı
    db = SessionLocal()
    try:
        print("Test kullanıcıları oluşturuluyor...")
        for user_data in test_users:
            # Kullanıcı zaten var mı kontrol et
            existing_user = crud.get_user_by_name(db, name=user_data["name"])
            if existing_user:
                print(f"Kullanıcı zaten mevcut: {user_data['name']}")
                continue
                
            # Yeni kullanıcı oluştur
            user = schemas.UserCreate(**user_data)
            db_user = crud.create_user(db, user)
            print(f"Kullanıcı oluşturuldu: {db_user.name} (ID: {db_user.id})")
            
        print("\nTüm test kullanıcıları oluşturuldu!")
        
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users() 