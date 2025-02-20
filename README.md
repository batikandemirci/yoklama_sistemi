# Video Tabanlı Yoklama Sistemi

Bu proje, yüz tanıma teknolojisi kullanarak video tabanlı bir yoklama sistemi oluşturmayı amaçlamaktadır. Sistem, canlı kamera görüntüsü veya yüklenmiş videolar üzerinden yüz tanıma yaparak otomatik yoklama alabilmektedir.

## 🚀 Özellikler

### ✅ Tamamlanan Özellikler

1. **Yüz Tanıma**
   - DeepFace ve MTCNN kullanarak yüz tespiti ve tanıma
   - Referans fotoğrafları ile yüz eşleştirme
   - Güven skoru hesaplama ve filtreleme
   - Çoklu yüz tanıma desteği

2. **Kullanıcı Yönetimi**
   - Kullanıcı ekleme, düzenleme ve silme
   - Rol tabanlı kullanıcı sistemi (öğrenci, öğretmen vb.)
   - Referans fotoğrafı yükleme ve güncelleme

3. **Yoklama Kayıtları**
   - Otomatik yoklama kaydı oluşturma
   - Günlük yoklama raporları
   - Kullanıcı bazlı yoklama geçmişi
   - Güven skoru ve zaman damgası ile kayıt

4. **API ve Frontend**
   - FastAPI ile RESTful API
   - React ile modern web arayüzü
   - Gerçek zamanlı video işleme
   - Responsive tasarım

### 🚧 Eksik/Geliştirilmesi Gereken Özellikler

1. **Video İşleme İyileştirmeleri**
   - Video işleme performansının optimizasyonu
   - Frame atlama mantığının iyileştirilmesi
   - Video durdurma/devam ettirme kontrolü
   - Video işleme progress bar'ı

2. **Yoklama Sistemi Geliştirmeleri**
   - Ders/sınıf bazlı yoklama tanımları
   - Özelleştirilebilir yoklama saatleri
   - Geç kalma toleransı ayarları
   - Otomatik yoklama raporu oluşturma
   - Gerçek zamanlı statik yerine dinamik yoklama alma

3. **Kullanıcı Arayüzü İyileştirmeleri**
   - Daha detaylı hata mesajları
   - Loading state'leri
   - Form validasyonları
   - Kullanıcı geri bildirimleri

4. **Güvenlik ve Performans**
   - JWT authentication
   - Rate limiting
   - Caching mekanizması
   - API endpoint optimizasyonları

## 🛠️ Teknolojiler

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- DeepFace
- MTCNN
- OpenCV
- TensorFlow

### Frontend
- React
- Next.js
- Tailwind CSS
- Axios

### Veritabanı
- SQLite (Geliştirme)
- PostgreSQL (Üretim için önerilen)

## 🚀 Kurulum

1. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Veritabanını oluşturun:
```bash
cd src
python database/init_db.py
```

3. Test kullanıcılarını oluşturun:
```bash
python scripts/create_test_users.py
```

4. Backend sunucusunu başlatın:
```bash
uvicorn main:app --reload
```

5. Frontend geliştirme sunucusunu başlatın:
```bash
cd frontend
npm install
npm run dev
```

## 📁 Proje Yapısı

```
src/
├── ai_module/              # Yüz tanıma modülü
├── backend/               # FastAPI backend
├── database/             # Veritabanı modelleri ve işlemleri
├── frontend/             # React frontend
├── scripts/              # Yardımcı scriptler
└── main.py              # Ana uygulama
```

## 🎯 Kullanım Senaryoları

1. **Yüz Kaydı**
   - Kullanıcı oluştur
   - Referans fotoğrafı yükle
   - Yüz tanıma testini gerçekleştir

2. **Yoklama Alma**
   - Video yükle veya kamera aç
   - Otomatik yüz tanıma
   - Yoklama kaydı oluşturma

3. **Raporlama**
   - Günlük yoklama görüntüleme
   - Kişi bazlı yoklama geçmişi
   - Yoklama istatistikleri

## 🔜 Gelecek Geliştirmeler

1. **Kamera Entegrasyonu**
   - Canlı kamera desteği
   - IP kamera entegrasyonu
   - Çoklu kamera desteği

2. **Akıllı Yoklama**
   - Ders programı entegrasyonu
   - Otomatik yoklama zamanları
   - Akıllı devamsızlık takibi

3. **Gelişmiş Raporlama**
   - PDF rapor çıktısı
   - E-posta bildirimleri
   - İstatistik grafikleri

4. **Mobil Uygulama**
   - iOS ve Android desteği
   - Mobil kamera ile yoklama
   - Push notifications

## 🤝 Katkıda Bulunma

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

## 👥 Yazarlar

- İsim Soyisim - [GitHub](github-link)

## 🙏 Teşekkürler

- DeepFace ekibine
- MTCNN geliştiricilerine
- FastAPI ve React topluluklarına 