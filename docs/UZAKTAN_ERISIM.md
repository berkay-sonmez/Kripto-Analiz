# 🌐 UZAKTAN ERİŞİM VE ARKA PLAN ÇALIŞTIRMA KILAVUZU

## 🎯 Amaç

Whale Alert Bot'u **24/7 çalıştırmak** ve **telefondan uzaktan kontrol etmek** için çözümler.

---

## ✅ Seçenek 1: Windows'ta Arka Planda Çalıştır (EN KOLAY)

### Nasıl Çalışır?
- Bot arka planda çalışır (pencere görünmez)
- Bilgisayar açık olmalı
- Telegram üzerinden bildirim alırsınız
- İnternet bağlantısı olmalı

### Kullanım

#### 1. Arka Planda Başlat
Desktop'ta veya klasörde **`START_HIDDEN.bat`** dosyasına çift tıklayın.

#### 2. Kontrol Et
Görev Yöneticisi → Ayrıntılar → `python.exe` var mı?

#### 3. Durdur
Görev Yöneticisi → `python.exe` → Sağ tık → "Görevi Sonlandır"

### Artıları:
- ✅ Çok kolay
- ✅ Ekstra maliyet yok
- ✅ Anında başlar

### Eksileri:
- ❌ Bilgisayar açık kalmalı
- ❌ İnternet kesintisinde durur

---

## 🌍 Seçenek 2: Uzak Masaüstü (RDP) - Orta Zorluk

### Nasıl Çalışır?
- Windows Uzak Masaüstü ile telefondan bilgisayara bağlanın
- Bot'u uzaktan başlatın/durdurun

### Kurulum

#### Windows'ta Uzak Masaüstü Aç
1. **Ayarlar** → **Sistem** → **Uzak Masaüstü**
2. "Uzak Masaüstü'nü Etkinleştir" → **Açık**
3. Bilgisayar adınızı not edin (örn: `DESKTOP-ABC123`)

#### Telefondan Bağlan
1. **Microsoft Remote Desktop** uygulamasını indirin (iOS/Android)
2. **+** → **PC Ekle**
3. **PC adı**: Bilgisayar adınız veya IP
4. Kullanıcı adı/şifre girin
5. Bağlan → Bot'u başlat!

### Artıları:
- ✅ Tam kontrol
- ✅ Her şeyi görebilirsiniz

### Eksileri:
- ❌ Aynı ağda olmalısınız (VPN gerekebilir)
- ❌ Bilgisayar açık kalmalı

---

## ☁️ Seçenek 3: Cloud Sunucu (VPS) - İLERİ SEVİYE

### Nasıl Çalışır?
- Bot'u bulut sunucuda çalıştırın (AWS, DigitalOcean, Hetzner)
- 24/7 çalışır, bilgisayarınız kapalı olabilir

### Kurulum (Özet)

#### 1. VPS Kiralayın
- **DigitalOcean**: $6/ay (Basic Droplet)
- **Hetzner Cloud**: €4/ay
- **AWS EC2**: Free tier (12 ay ücretsiz)

#### 2. Windows Server Kurun
VPS'ye Windows Server 2022 yükleyin.

#### 3. Projeyi Yükleyin
RDP ile bağlanın → Projeyi kopyalayın → Bot'u başlatın

#### 4. Telegram'dan Takip Edin
Artık bot 7/24 çalışır, siz sadece Telegram'dan bildirim alırsınız!

### Artıları:
- ✅ 7/24 çalışır
- ✅ Bilgisayarınız kapalı olabilir
- ✅ İnternet kesintisi yok

### Eksileri:
- ❌ Aylık ~$5-10 maliyet
- ❌ Teknik bilgi gerekir

---

## 📱 Seçenek 4: Teamviewer/AnyDesk - Kolay Uzaktan Erişim

### Nasıl Çalışır?
- Telefondan bilgisayarınıza bağlanın
- Bot'u uzaktan başlatın/durdurun

### Kurulum

#### 1. TeamViewer Kur
- Bilgisayara: https://www.teamviewer.com/tr/
- Telefona: TeamViewer uygulamasını indirin

#### 2. ID ve Şifre Al
TeamViewer açıldığında "Your ID" ve "Password" görürsünüz.

#### 3. Telefondan Bağlan
Telefon uygulamasında ID'yi girin → Bağlan!

### Artıları:
- ✅ Çok kolay
- ✅ Her yerden bağlanırsınız
- ✅ Ücretsiz (kişisel kullanım)

### Eksileri:
- ❌ Bilgisayar açık kalmalı

---

## 🎯 ÖNERİLEN KURULUM

### Ev Kullanımı (Bilgisayar 7/24 Açık Kalabilir)

1. **START_HIDDEN.bat** ile arka planda çalıştırın
2. **TeamViewer** kurun (uzaktan kontrol için)
3. Telegram'dan bildirimleri takip edin

**Neden?**
- ✅ Ekstra maliyet yok
- ✅ Kolay kurulum
- ✅ İhtiyaç olunca TeamViewer ile uzaktan erişim

---

### Profesyonel Kullanım (7/24 Kesintisiz)

1. **VPS kiralayın** (DigitalOcean/Hetzner)
2. Bot'u VPS'de çalıştırın
3. Telegram'dan takip edin

**Neden?**
- ✅ 7/24 çalışır
- ✅ Elektrik kesintisi etkilemez
- ✅ İnternet sorunu olmaz

---

## 🔧 Windows Görev Zamanlayıcı ile Otomatik Başlatma

Bot'u **Windows başladığında otomatik** başlat:

### Adımlar

1. **Görev Zamanlayıcı** açın (Task Scheduler)
2. **Temel Görev Oluştur**
3. Ad: "Whale Alert Bot"
4. Tetikleyici: "Bilgisayar başladığında"
5. Eylem: **Program Başlat**
   - Program: `C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz\START_HIDDEN.bat`
6. Tamam → Kaydet

Artık bilgisayar her açıldığında bot otomatik başlar!

---

## ❓ SSS

### Bot çalışıyor mu nasıl anlarım?
**Yöntem 1:** Telegram'a test mesajı geldi mi?
**Yöntem 2:** Görev Yöneticisi → `python.exe` var mı?

### Bot'u nasıl durdururum?
Görev Yöneticisi → `python.exe` → Sağ tık → "Görevi Sonlandır"

### Bilgisayar uyku moduna geçerse ne olur?
Bot durur! **Ayarlar** → **Güç ve Pil** → **Ekran** = 30 dk, **Uyku** = Asla

### İnternet kesilirse?
Bot durur. İnternet gelince tekrar başlatmalısınız (veya otomatik başlatma kurun).

### VPS'ye nasıl yüklerim?
1. VPS'ye RDP ile bağlan
2. Python 3.13 kur
3. Projeyi git clone veya kopyala
4. `pip install -r requirements.txt`
5. `.env` dosyasını düzenle
6. `START_HIDDEN.bat` çalıştır

---

## ✅ Önerilen Seçim: Kullanım Senaryonuza Göre

| Senaryo | Öneri | Maliyet | Zorluk |
|---------|-------|---------|--------|
| Gündüz çalışsın | START_HIDDEN.bat | Ücretsiz | ⭐ Kolay |
| Uzaktan kontrol | TeamViewer + START_HIDDEN | Ücretsiz | ⭐⭐ Orta |
| 7/24 kesintisiz | VPS (Hetzner/DigitalOcean) | $5/ay | ⭐⭐⭐ İleri |
| Profesyonel | VPS + Monitoring | $10/ay | ⭐⭐⭐⭐ İleri |

---

## 🚀 Hızlı Başlangıç

**Şimdi ne yapmalıyım?**

1. **`START_HIDDEN.bat`** dosyasına çift tıklayın
2. Görev Yöneticisi'nde `python.exe` var mı kontrol edin
3. Telegram'dan ilk bildirimi bekleyin
4. İsteğe bağlı: **TeamViewer** kurun (uzaktan erişim için)

İyi işlemler! 🎉
