import os
from pathlib import Path
import shutil

# Klasör yolları
DATA_DIR = Path(__file__).parent.parent.parent / "data"
TEST_IMAGES_DIR = DATA_DIR / "test_images"

# Kullanıcı bilgileri
users = {
    "hugh": {"id": 12, "old_name": "hugh_jackman"},
    "robert": {"id": 13, "old_name": "robert_downey_jr"},
    "johnny": {"id": 14, "old_name": "johnny_depp"},
    "megan": {"id": 15, "old_name": "megan_fox"}
}

def clean_old_photos():
    """Eski fotoğrafları temizle"""
    print("\nEski fotoğraflar temizleniyor...")
    for name, info in users.items():
        # Kullanıcının tüm eski fotoğraflarını bul
        old_photos = list(TEST_IMAGES_DIR.glob(f"{info['old_name']}*.jpg"))
        for photo in old_photos:
            try:
                os.remove(photo)
                print(f"✓ Silindi: {photo.name}")
            except Exception as e:
                print(f"✗ Silinemedi: {photo.name} ({e})")

def rename_photos():
    """Fotoğrafları doğru formatta yeniden adlandır"""
    print("\nFotoğraflar yeniden adlandırılıyor...")
    
    for name, info in users.items():
        # Kullanıcının ilk fotoğrafını bul
        old_photos = list(TEST_IMAGES_DIR.glob(f"{info['old_name']} (1).jpg"))
        if not old_photos:
            # Eğer (1) formatında bulunamazsa, diğer formatlarda dene
            old_photos = list(TEST_IMAGES_DIR.glob(f"{info['old_name']}*.jpg"))
            
        if old_photos:
            # İlk fotoğrafı al
            old_photo = old_photos[0]
            # Yeni isim formatı
            new_name = f"{name}_{info['id']}.jpg"
            new_path = TEST_IMAGES_DIR / new_name
            
            try:
                # Fotoğrafı kopyala
                shutil.copy2(old_photo, new_path)
                print(f"✓ {old_photo.name} -> {new_name}")
            except Exception as e:
                print(f"✗ Hata: {e}")
        else:
            print(f"✗ {info['old_name']} için fotoğraf bulunamadı!")

if __name__ == "__main__":
    rename_photos()
    clean_old_photos()
    print("\nİşlem tamamlandı!") 