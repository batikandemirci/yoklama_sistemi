# Kamera Tabanlı Yoklama Sistemi

![Kullanıcılar](https://github.com/user-attachments/assets/d96b31f0-cccf-4ac4-8081-2097d5f5c3c8)
![Yoklama al](https://github.com/user-attachments/assets/721a11c4-9dc8-4101-95e7-3b914972f4d6)
![Yoklama Kayıtları](https://github.com/user-attachments/assets/f1989917-5225-4672-ba32-0b15b393e2a4)

Türkiye'de hala birçok eğitim kurumunda yoklamalar kağıt üzerinde alınıyor. Bu durumu değiştirmek için bir adım atmak istedim ve kamera&video tabanlı bir yoklama sistemi geliştirdim.

🎯 Mevcut Durum ve Hedef:
• Günde ortalama 5-10 dakika yoklama işlemlerine harcanıyor
• Kağıt israfı ve arşivleme zorlukları yaşanıyor
• Manuel işlemlerde insan kaynaklı hatalar oluşabiliyor

💡 Geliştirdiğim Sistem:
• Video veya kamera üzerinden yüz tanıma ile yoklama
• Basit ve kullanıcı dostu arayüz
• Şimdilik yarı-dinamik kayıt ve raporlama

⚠️ Mevcut Sınırlamalar:
• Yüz tanıma doğruluk oranı geliştirilebilir (%60-70 civarı)
• Kalabalık sınıflarda performans düşüşü
• Aydınlatma koşullarına bağımlılık
• Video işleme süresinin optimizasyon ihtiyacı

🛠️ Kullanılan Teknolojiler:
• Backend: Python, FastAPI, SQLAlchemy
• AI: DeepFace, MTCNN, OpenCV, TensorFlow
• Frontend: React, Next.js, Tailwind CSS
• Database: PostgreSQL

🔄 Gelecek Geliştirmeler:
• Tam otonom bir sistem olması
• Veri tabanı entegrasyonun iyileştirilmesi
• Doğruluk oranının artırılması
• Performans optimizasyonu
• Gerçek zamanlı işleme kapasitesi

Bu proje, eğitimde dijital dönüşüm yolculuğunda atılmış küçük bir adım. Henüz mükemmel değil, ama geliştirilmeye açık bir başlangıç.


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

- Batıkan DEMİRCİ - [GitHub]([github-link](https://github.com/batikandemirci))

## 🙏 Teşekkürler

- DeepFace ekibine
- MTCNN geliştiricilerine
- FastAPI ve React topluluklarına 
