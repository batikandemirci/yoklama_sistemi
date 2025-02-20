import os
import zipfile
from pathlib import Path
import shutil
import logging
from tqdm import tqdm

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

def create_directories():
    """Gerekli klasörleri oluştur"""
    for directory in [TEST_IMAGES_DIR, TEST_VIDEOS_DIR, FACE_EMBEDDINGS_DIR, MODELS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Klasör oluşturuldu: {directory}")

def extract_and_organize(zip_path: Path):
    """Kaggle'dan indirilen ZIP dosyasını çıkart ve organize et"""
    try:
        # Klasörleri oluştur
        create_directories()
        
        # ZIP dosyasının varlığını kontrol et
        if not zip_path.exists():
            logger.error(f"ZIP dosyası bulunamadı: {zip_path}")
            return False
        
        logger.info("ZIP dosyası çıkartılıyor...")
        # Doğrudan test_images klasörüne çıkart
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Tüm dosyaları listele
            files = zip_ref.namelist()
            
            # JPG dosyalarını filtrele
            jpg_files = [f for f in files if f.lower().endswith('.jpg')]
            
            logger.info(f"Toplam {len(jpg_files)} fotoğraf bulundu")
            logger.info("Fotoğraflar test_images klasörüne çıkartılıyor...")
            
            for jpg_file in tqdm(jpg_files, desc="Fotoğraflar işleniyor"):
                zip_ref.extract(jpg_file, TEST_IMAGES_DIR)
        
        # Toplam fotoğraf sayısını göster
        total_images = len(list(TEST_IMAGES_DIR.glob("*.jpg")))
        logger.info(f"Toplam {total_images} fotoğraf başarıyla işlendi")
        
        return True
        
    except Exception as e:
        logger.error(f"Veri organizasyon hatası: {e}")
        return False

if __name__ == "__main__":
    # Kaggle'dan indirilen ZIP dosyasının yolu
    kaggle_zip = DATA_DIR / "lfw-people.zip"
    
    if not kaggle_zip.exists():
        logger.error("""
        Lütfen aşağıdaki adımları takip edin:
        1. https://www.kaggle.com/datasets/vishesh1412/celebrity-face-image-dataset adresinden veri setini indirin
        2. İndirilen ZIP dosyasını 'data' klasörüne 'lfw-people.zip' olarak kopyalayın
        3. Bu scripti tekrar çalıştırın
        """)
    else:
        extract_and_organize(kaggle_zip) 