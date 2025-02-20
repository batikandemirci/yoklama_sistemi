# Donanım Planlaması Dokümanı

## 1. Test Ortamı Gereksinimleri

### 1.1 Geliştirme Ortamı
- İşlemci: Minimum Intel i5 veya AMD Ryzen 5
- RAM: Minimum 8GB
- Depolama: Minimum 256GB SSD
- İşletim Sistemi: Windows 11
- Python Sürümü: 3.10

### 1.2 Test Veri Seti Gereksinimleri
- Minimum 100 farklı yüz görüntüsü
- En az 10 farklı test videosu
- Her video minimum 30 saniye uzunluğunda
- Video çözünürlüğü: 1080p (1920x1080)
- FPS: 30

### 1.3 Veri Depolama Yapısı
```
data/
├── test_images/          # Test için kullanılacak yüz görüntüleri
├── test_videos/          # Test için kullanılacak video kayıtları
├── face_embeddings/      # İşlenmiş yüz vektörleri
└── models/              # Eğitilmiş modeller ve ağırlıklar
```

## 2. Üretim Ortamı Planlaması (Gelecek)

### 2.1 Kamera Gereksinimleri
- Çözünürlük: Minimum 1080p (1920x1080)
- FPS: Minimum 30fps
- Görüş Açısı: Minimum 90 derece
- Gece Görüşü: IR destekli
- Bağlantı: PoE (Power over Ethernet)

### 2.2 Edge Computing Gereksinimleri
- İşlemci: NVIDIA Jetson Nano veya eşdeğeri
- RAM: Minimum 4GB
- Depolama: Minimum 64GB
- Network: Gigabit Ethernet

### 2.3 Network Gereksinimleri
- Bant Genişliği: Minimum 100Mbps
- Latency: Maximum 50ms
- Protokol: TCP/IP, RTSP
- Güvenlik: SSL/TLS

## 3. Test Veri Seti Özellikleri

### 3.1 Test Görüntüleri
- Format: JPG/PNG
- Çözünürlük: Minimum 640x480
- Kişi Başı Görüntü: Minimum 5 farklı açı
- Işık Koşulları: Farklı aydınlatma senaryoları

### 3.2 Test Videoları
- Format: MP4/AVI
- Codec: H.264
- Bit Rate: 4-8 Mbps
- Ses: Gerekli değil
- Süre: 30-60 saniye

## 4. Performans Metrikleri

### 4.1 İşlem Süreleri
- Yüz Tespiti: <100ms
- Yüz Tanıma: <200ms
- Toplam İşlem: <500ms

### 4.2 Doğruluk Oranları
- Yüz Tespiti: >99%
- Yüz Tanıma: >95%
- Yanlış Pozitif Oranı: <1% 