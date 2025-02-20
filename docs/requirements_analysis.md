# Akıllı Yoklama Sistemi Gereksinim Analizi

## 1. Sistem Gereksinimleri

### 1.1 Fonksiyonel Gereksinimler

#### Yüz Tanıma ve Yoklama
- Sınıf girişinde öğrenci yüzlerinin otomatik tespiti
- Gerçek zamanlı yüz tanıma ve eşleştirme
- Yoklamanın otomatik olarak sisteme işlenmesi
- Çoklu yüz tespiti ve işleme kapasitesi

#### Veri Yönetimi
- Öğrenci bilgilerinin güvenli depolanması
- Yüz verilerinin şifreli olarak saklanması
- Yoklama kayıtlarının tarih ve saat bilgisiyle tutulması
- Geçmiş yoklama verilerine erişim

#### Raporlama
- Günlük, haftalık ve aylık yoklama raporları
- Öğrenci bazlı devam durumu analizi
- Sınıf bazlı devam durumu analizi
- PDF ve Excel formatında rapor çıktıları

### 1.2 Teknik Gereksinimler

#### Donanım (Test Aşaması İçin)
- Test videoları ve görüntüleri
- Minimum 8GB RAM'li geliştirme bilgisayarı
- Stabil internet bağlantısı

#### Yazılım
- Python 3.10
- PostgreSQL veritabanı
- FastAPI web framework
- OpenCV ve DeepFace kütüphaneleri

#### Güvenlik
- KVKK uyumlu veri saklama
- Şifreli veri iletişimi
- Rol tabanlı erişim kontrolü
- Güvenli kimlik doğrulama

### 1.3 Kullanıcı Gereksinimleri

#### Öğretmenler İçin
- Kolay kullanılabilir web arayüzü
- Manuel yoklama düzenleme imkanı
- Anlık yoklama durumu görüntüleme
- Raporlama araçlarına kolay erişim

#### Yöneticiler İçin
- Sistem durumu izleme
- Kullanıcı yönetimi
- Genel raporlama ve analiz
- Sistem ayarları yapılandırma

#### Öğrenciler İçin
- Kendi yoklama durumlarını görüntüleme
- Devamsızlık bilgisi takibi
- İtiraz/düzeltme talep etme

## 2. Kısıtlamalar ve Riskler

### 2.1 Teknik Kısıtlamalar
- Test aşamasında gerçek kamera olmaması
- Yüz tanıma doğruluk oranı limitleri
- Sistem performans limitleri

### 2.2 Riskler
- Yüz tanıma hataları
- Sistem yanıt süresi gecikmeleri
- Veri güvenliği riskleri

## 3. Başarı Kriterleri

### 3.1 Performans Kriterleri
- Yüz tanıma başarı oranı: >95%
- Sistem yanıt süresi: <2 saniye
- Eşzamanlı kullanıcı desteği: >50 kullanıcı

### 3.2 Güvenilirlik Kriterleri
- Sistem uptime: >99%
- Veri kaybı: 0%
- Yanlış yoklama kaydı: <1% 