import requests
import os
from pathlib import Path
import time

# API endpoint
API_URL = "http://localhost:8000/face-recognition/recognize-video"

# Test dosyaları yolu
DATA_DIR = Path(__file__).parent.parent.parent / "data"
TEST_VIDEOS_DIR = DATA_DIR / "test_videos"

def test_video_recognition(video_path):
    """Video üzerinde yüz tanıma testini gerçekleştir"""
    print(f"\nTest ediliyor: {video_path.name}")
    print("=" * 50)
    
    with open(video_path, "rb") as file:
        files = {"file": (video_path.name, file, "video/mp4")}
        response = requests.post(API_URL, files=files)
        
        result = response.json()
        
        # İşlem bilgilerini göster
        if "processed_frames" in result and "total_frames" in result:
            print(f"\nİşlenen frame: {result['processed_frames']}/{result['total_frames']}")
            print(f"İşleme oranı: {(result['processed_frames']/result['total_frames']*100):.1f}%")
        
        # Minimum güven skorunu göster
        if "min_confidence" in result:
            print(f"Minimum güven skoru: {result['min_confidence']:.2f}")
            
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
            
    # Her test arasında 2 saniye bekle
    time.sleep(2)

if __name__ == "__main__":
    # Önce tekli kişi videolarını test et
    print("\n=== TEKLİ KİŞİ VİDEOLARI TESTİ ===")
    single_person_videos = sorted(TEST_VIDEOS_DIR.glob("single_person_*.mp4"))
    for video_path in single_person_videos:
        test_video_recognition(video_path)
        
    # Sonra çoklu kişi videolarını test et
    print("\n=== ÇOKLU KİŞİ VİDEOLARI TESTİ ===")
    multi_person_videos = sorted(TEST_VIDEOS_DIR.glob("multi_person_*.mp4"))
    for video_path in multi_person_videos:
        test_video_recognition(video_path) 