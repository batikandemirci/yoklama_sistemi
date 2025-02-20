import cv2
import numpy as np
from pathlib import Path
import random
import logging
from tqdm import tqdm
import shutil
import os

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
TEMP_DIR = DATA_DIR / 'temp_images'

def create_single_person_video(person_name: str, output_path: Path, duration_seconds: int = 30, fps: int = 30):
    """Tek kişilik test videosu oluştur"""
    try:
        # Sabit frame boyutu
        TARGET_SIZE = (224, 224)  # Standart bir boyut
        
        # Kişinin tüm fotoğraflarını bul
        person_images = list(TEST_IMAGES_DIR.glob(f"{person_name}*.jpg"))
        if not person_images:
            logger.error(f"{person_name} için fotoğraf bulunamadı")
            return False
            
        frames = []
        for img_path in person_images:
            # Mutlak dosya yolunu al ve normalize et
            absolute_path = str(img_path.absolute())
            normalized_path = os.path.normpath(absolute_path)
            frame = cv2.imread(normalized_path)
            if frame is not None:
                # Frame'i hedef boyuta yeniden boyutlandır
                frame = cv2.resize(frame, TARGET_SIZE)
                frames.append(frame)
        
        if not frames:
            logger.error(f"Hiçbir fotoğraf okunamadı: {person_name}")
            return False
            
        height, width = TARGET_SIZE
        
        # Geçici video dosyası oluştur
        temp_output = output_path.with_suffix('.temp.mp4')
        
        # Video yazıcıyı ayarla
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(temp_output), fourcc, fps, (width, height))
        
        total_frames = duration_seconds * fps
        
        # Her frame için
        for _ in tqdm(range(total_frames), desc=f"{output_path.name} oluşturuluyor"):
            # Rastgele bir frame seç
            frame = random.choice(frames)
            
            # Frame'i videoya yaz
            out.write(frame)
        
        out.release()
        
        # FFmpeg ile web uyumlu formata dönüştür
        os.system(f'ffmpeg -y -i "{temp_output}" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k "{output_path}"')
        
        # Geçici dosyayı sil
        temp_output.unlink()
        
        # Geçici klasörü temizle
        temp_person_dir = TEMP_DIR / person_name
        temp_person_dir.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(temp_person_dir)
        
        logger.info(f"Video oluşturuldu: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Video oluşturma hatası: {e}")
        return False

def create_multi_person_video(person_names: list, output_path: Path, duration_seconds: int = 30, fps: int = 30):
    """Çoklu kişi içeren test videosu oluştur"""
    try:
        # Sabit frame boyutu
        TARGET_SIZE = (224, 224)  # Standart bir boyut
        
        # Her kişi için fotoğrafları hazırla
        person_frames = {}
        
        for person in person_names:
            person_frames[person] = []
            images = list(TEST_IMAGES_DIR.glob(f"{person}*.jpg"))
            
            if images:
                for img_path in images:
                    # Mutlak dosya yolunu al ve normalize et
                    absolute_path = str(img_path.absolute())
                    normalized_path = os.path.normpath(absolute_path)
                    frame = cv2.imread(normalized_path)
                    if frame is not None:
                        # Frame'i hedef boyuta yeniden boyutlandır
                        frame = cv2.resize(frame, TARGET_SIZE)
                        person_frames[person].append(frame)
        
        # Boş frame listesi olan kişileri temizle
        person_frames = {k: v for k, v in person_frames.items() if v}
        
        if not person_frames:
            logger.error("Fotoğraflar okunamadı")
            return False
            
        height, width = TARGET_SIZE
        grid_size = int(np.ceil(np.sqrt(len(person_names))))
        
        # Geçici video dosyası oluştur
        temp_output = output_path.with_suffix('.temp.mp4')
        
        # Video yazıcıyı ayarla
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            str(temp_output), 
            fourcc, 
            fps, 
            (width * grid_size, height * grid_size)
        )
        
        total_frames = duration_seconds * fps
        
        # Her frame için
        for _ in tqdm(range(total_frames), desc=f"{output_path.name} oluşturuluyor"):
            # Boş grid oluştur
            grid = np.zeros((height * grid_size, width * grid_size, 3), dtype=np.uint8)
            
            # Her kişi için rastgele bir fotoğraf seç ve grid'e yerleştir
            for idx, person in enumerate(person_frames.keys()):
                row = idx // grid_size
                col = idx % grid_size
                
                # Rastgele bir frame seç
                frame = random.choice(person_frames[person])
                
                # Grid'e yerleştir
                grid[row*height:(row+1)*height, col*width:(col+1)*width] = frame
            
            # Frame'i videoya yaz
            out.write(grid)
        
        out.release()
        
        # FFmpeg ile web uyumlu formata dönüştür
        os.system(f'ffmpeg -y -i "{temp_output}" -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 128k "{output_path}"')
        
        # Geçici dosyayı sil
        temp_output.unlink()
        
        # Geçici klasörleri temizle
        for person in person_names:
            temp_person_dir = TEMP_DIR / person
            if temp_person_dir.exists():
                shutil.rmtree(temp_person_dir)
        
        logger.info(f"Video oluşturuldu: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Video oluşturma hatası: {e}")
        return False

def create_test_videos():
    """Test videolarını oluştur"""
    try:
        # Test videoları ve geçici klasörü oluştur
        TEST_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        
        # Mevcut kişilerin listesini al
        all_images = list(TEST_IMAGES_DIR.glob("*.jpg"))
        unique_persons = set()
        
        for img_path in all_images:
            person_name = img_path.stem.split('_')[0]
            unique_persons.add(person_name)
        
        unique_persons = list(unique_persons)
        logger.info(f"Toplam {len(unique_persons)} farklı kişi bulundu: {', '.join(unique_persons)}")
        
        # Kullanılmamış kişileri takip et
        available_persons = unique_persons.copy()
        
        # 5 adet tek kişilik video oluştur
        for i in range(5):
            if not available_persons:  # Eğer tüm kişiler kullanıldıysa listeyi yenile
                available_persons = unique_persons.copy()
                
            person = random.choice(available_persons)
            available_persons.remove(person)  # Kullanılan kişiyi listeden çıkar
            
            output_path = TEST_VIDEOS_DIR / f"single_person_{i+1}.mp4"
            logger.info(f"Tek kişilik video {i+1} oluşturuluyor - Kişi: {person}")
            create_single_person_video(person, output_path, fps=10)  # FPS'i 10'a düşür
        
        # Kullanılmamış kişiler listesini yenile
        available_persons = unique_persons.copy()
        
        # 5 adet çoklu kişi videosu oluştur (2-4 kişi)
        for i in range(5):
            if len(available_persons) < 4:  # Eğer yeterli kişi kalmadıysa listeyi yenile
                available_persons = unique_persons.copy()
                
            num_people = random.randint(2, min(4, len(available_persons)))
            selected_people = random.sample(available_persons, num_people)
            
            # Seçilen kişileri listeden çıkar
            for person in selected_people:
                available_persons.remove(person)
                
            output_path = TEST_VIDEOS_DIR / f"multi_person_{i+1}.mp4"
            logger.info(f"Çoklu kişi videosu {i+1} oluşturuluyor - Kişiler: {', '.join(selected_people)}")
            create_multi_person_video(selected_people, output_path, fps=10)  # FPS'i 10'a düşür
            
        # Geçici klasörü temizle
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)
            
        logger.info("Tüm test videoları oluşturuldu")
        return True
        
    except Exception as e:
        logger.error(f"Test video oluşturma hatası: {e}")
        return False

if __name__ == "__main__":
    create_test_videos() 