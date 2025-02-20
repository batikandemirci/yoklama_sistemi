import requests
import os
from pathlib import Path

# API endpoint
API_URL = "http://localhost:8000/face-recognition/recognize"

# Test dosyaları yolu
DATA_DIR = Path(__file__).parent.parent.parent / "data"
TEST_IMAGES_DIR = DATA_DIR / "test_images"

def test_recognition(image_path):
    """Görüntü üzerinde yüz tanıma testini gerçekleştir"""
    print(f"\nTest ediliyor: {image_path.name}")
    
    with open(image_path, "rb") as file:
        files = {"file": (image_path.name, file, "image/jpeg")}
        response = requests.post(API_URL, files=files)
        
        result = response.json()
        
        # Minimum güven skorunu göster
        if "min_confidence" in result:
            print(f"\nMinimum güven skoru: {result['min_confidence']:.2f}")
            
        # Sonuç mesajını göster
        if "message" in result:
            print(f"Sonuç: {result['message']}")
            
        if "recognized_people" in result:
            if result["recognized_people"]:
                print("\nTanınan Kişiler:")
                print("-" * 50)
                for person in result["recognized_people"]:
                    print(f"İsim: {person['name']}")
                    print(f"Güven: {person['confidence']:.2f}")
                    
                    # Yoklama durumunu göster
                    status_messages = {
                        "recorded": "✓ Yeni kayıt (ID: {})".format(person.get("attendance_id", "?")),
                        "already_attended": "⚠ Bugün zaten katılmış",
                        "not_recorded": "✗ Kaydedilemedi",
                        "error": "❌ Hata oluştu"
                    }
                    status = person.get("attendance_status", "not_recorded")
                    print(f"Yoklama Durumu: {status_messages[status]}")
                    print("-" * 50)
            else:
                print("Kimse tanınamadı.")
        
        if "error" in result:
            print(f"Hata: {result['error']}")

if __name__ == "__main__":
    # Test fotoğraflarını bul
    test_images = list(TEST_IMAGES_DIR.glob("*.jpg"))
    
    if not test_images:
        print("Test klasöründe fotoğraf bulunamadı!")
    else:
        # İlk fotoğrafı test et
        test_recognition(test_images[0]) 