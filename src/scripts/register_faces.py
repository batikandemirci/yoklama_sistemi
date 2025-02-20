import requests
import os
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/face-recognition/register-face"

# Klasör yolları
DATA_DIR = Path(__file__).parent.parent.parent / "data"
TEST_IMAGES_DIR = DATA_DIR / "test_images"

# Kullanıcı bilgileri
users = {
    "hugh": {"id": 12, "filename": "hugh_12.jpg"},
    "robert": {"id": 13, "filename": "robert_13.jpg"},
    "johnny": {"id": 14, "filename": "johnny_14.jpg"},
    "megan": {"id": 15, "filename": "megan_15.jpg"}
}

def register_faces():
    """Her kullanıcı için referans fotoğrafını kaydet"""
    print("\nReferans fotoğrafları kaydediliyor...")
    
    for name, info in users.items():
        photo_path = TEST_IMAGES_DIR / info["filename"]
        if not photo_path.exists():
            print(f"✗ Fotoğraf bulunamadı: {info['filename']}")
            continue
            
        print(f"\nKullanıcı: {name} (ID: {info['id']})")
        print(f"Fotoğraf: {info['filename']}")
        
        try:
            # Fotoğrafı gönder
            with open(photo_path, "rb") as file:
                files = {"file": (info["filename"], file, "image/jpeg")}
                response = requests.post(
                    f"{API_URL}/{info['id']}", 
                    files=files
                )
                
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Başarıyla kaydedildi (Güven: {result['confidence']:.2f})")
            else:
                print(f"✗ Hata: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"✗ Hata: {e}")

if __name__ == "__main__":
    register_faces()
    print("\nİşlem tamamlandı!") 