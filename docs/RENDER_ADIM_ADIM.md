# 🚀 RENDER.COM DEPLOYMENT - ADIM ADIM

## ✅ MEVCUT DURUM

Tüm dosyalar hazır:
- ✅ render.yaml
- ✅ start.sh
- ✅ Procfile
- ✅ runtime.txt
- ✅ whale_alert_bot_v2.py (headless Chrome)
- ✅ requirements.txt
- ✅ .env (Telegram token/chat ID)

---

## 🎯 ADIM 1: GIT KURULUMU (5 Dakika)

### Git Nedir?
GitHub'a kod yüklemek için gerekli araç.

### Kurulum:

**A. Git İndir**
```
1. https://git-scm.com/download/win adresine git
2. "64-bit Git for Windows Setup" indir
3. Kurulumu başlat
```

**B. Kurulum Ayarları** (Önemli!)
```
1. "Select Components" ekranı:
   ✅ Git Bash Here
   ✅ Git GUI Here
   ✅ Git LFS (Large File Support)

2. "Choosing the default editor":
   → "Use Visual Studio Code" (varsa)
   → Yoksa "Use Notepad" seç

3. "Adjusting your PATH":
   → "Git from the command line and also from 3rd-party software"
   (Ortadaki seçenek - önerilen)

4. "Choosing HTTPS transport backend":
   → "Use the OpenSSL library"

5. "Configuring line ending conversions":
   → "Checkout Windows-style, commit Unix-style line endings"

6. Geri kalan her şeyde "Next" → "Install"
```

**C. Kurulum Sonrası Test**
```powershell
# PowerShell'i KAPAT ve YENİDEN AÇ!
# Sonra:
git --version

# Çıktı: git version 2.42.0.windows.1 (veya benzeri)
```

**D. Git Kullanıcı Ayarları**
```powershell
# Adını ayarla
git config --global user.name "Berkay"

# Email'ini ayarla (GitHub email'in)
git config --global user.email "berkaysnmz1903@gmail.com"

# Kontrol et
git config --list
```

---

## 🎯 ADIM 2: GITHUB HESABI (2 Dakika)

### A. GitHub Kaydı

**Zaten hesabın varsa bu adımı atla!**

```
1. https://github.com adresine git
2. "Sign up" tıkla
3. Email: berkaysnmz1903@gmail.com
4. Password: Güçlü bir şifre oluştur
5. Username: Kullanıcı adı seç (örn: berkaysnmz)
6. Email doğrulama yap
```

### B. Personal Access Token Oluştur

Git push yaparken şifre yerine token kullanacağız.

```
1. GitHub'a giriş yap
2. Sağ üst → Profil fotoğrafı → Settings
3. Sol menü en altta → Developer settings
4. Personal access tokens → Tokens (classic)
5. "Generate new token" → "Generate new token (classic)"
6. Ayarlar:
   Note: "Kripto-Analiz Deploy"
   Expiration: 90 days
   Scopes: ✅ repo (tüm kutucuklar)
7. "Generate token" butonu
8. 🔴 ÖNEMLİ: Token'ı KOPYALA ve KAYDET!
   (Bu sayfadan çıkarsan bir daha göremezsin!)
```

**Token Örneği:**
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Not defterine yapıştır ve sakla!**

---

## 🎯 ADIM 3: GITHUB REPOSITORY OLUŞTUR (3 Dakika)

### A. Yeni Repository

```
1. GitHub ana sayfa → "New" butonu (yeşil, sağ üstte)
   VEYA
   https://github.com/new

2. Ayarlar:
   Repository name: Kripto-Analiz
   Description: 24/7 Whale Alert Bot with Telegram Notifications
   Visibility: 🔒 Private (ÖNEMLİ! - API key'ler gizli kalsın)
   
   ❌ Initialize repository seçeneklerini BOŞTA BIRAK!
   (README, .gitignore, license ekleme)

3. "Create repository" butonu
```

### B. Repository URL'sini Kopyala

Repo oluşturduktan sonra:
```
"Quick setup" sayfasında HTTPS URL'ini kopyala:
https://github.com/KULLANICI_ADIN/Kripto-Analiz.git

Örnek:
https://github.com/berkaysnmz/Kripto-Analiz.git
```

---

## 🎯 ADIM 4: PROJEYI GIT'E HAZIRLA (5 Dakika)

### A. Git Başlat

```powershell
# Proje dizininde
cd C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz

# Git başlat
git init

# Çıktı: Initialized empty Git repository in ...
```

### B. .env Dosyasını Gizle

⚠️ **ÖNEMLİ**: .env dosyası API key'ler içeriyor, GitHub'a yüklememek lazım!

```powershell
# .gitignore dosyası zaten var, kontrol et
notepad .gitignore

# İçinde şunlar olmalı:
# .env
# *.env
# chromedriver.exe
```

### C. Dosyaları Ekle

```powershell
# Tüm dosyaları staging area'ya ekle
git add .

# Durumu kontrol et
git status

# Yeşil yazılar göreceksin:
# new file: render.yaml
# new file: start.sh
# new file: whale_alert_bot_v2.py
# vs.

# Kırmızı yazılar: Eklenmemiş dosyalar
# .env KESİNLİKLE kırmızı olmalı (GitHub'a gitmesin!)
```

### D. İlk Commit

```powershell
# Commit yap
git commit -m "Initial commit - Whale Alert Bot with Render.com support"

# Çıktı: [main (root-commit) abc1234] ...
```

### E. Main Branch Oluştur

```powershell
# Branch adını main yap (GitHub standart)
git branch -M main
```

### F. GitHub'a Bağla

```powershell
# Remote ekle (URL'ini KULLANICI_ADIN ile değiştir!)
git remote add origin https://github.com/KULLANICI_ADIN/Kripto-Analiz.git

# Örnek:
# git remote add origin https://github.com/berkaysnmz/Kripto-Analiz.git

# Kontrol et
git remote -v
```

---

## 🎯 ADIM 5: GITHUB'A PUSH (2 Dakika)

### A. Push Komutu

```powershell
# Push yap
git push -u origin main
```

### B. Kullanıcı Adı/Token Girişi

Terminal şunları soracak:
```
Username for 'https://github.com': 
→ GitHub kullanıcı adını gir (örn: berkaysnmz)

Password for 'https://berkaysnmz@github.com':
→ ŞIFRE DEĞİL! Personal Access Token'ı yapıştır!
→ ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **ÖNEMLİ**: Password kısmına ŞIFRE DEĞİL TOKEN yapıştır!

### C. Başarılı Push

```
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
...
To https://github.com/berkaysnmz/Kripto-Analiz.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### D. GitHub'da Kontrol

```
1. https://github.com/KULLANICI_ADIN/Kripto-Analiz adresine git
2. Dosyalar görünmeli:
   ✅ render.yaml
   ✅ start.sh
   ✅ scripts/whale_alert_bot_v2.py
   ✅ requirements.txt
   ❌ .env (görünmemeli - gizli!)
```

---

## 🎯 ADIM 6: RENDER.COM KAYDOLMA (2 Dakika)

### A. Render'a Git

```
https://render.com
```

### B. Sign Up

```
1. "Get Started" veya "Sign Up" butonu
2. "Sign up with GitHub" seç (kolay entegrasyon)
3. GitHub'a yönlendirecek
4. GitHub'da "Authorize Render" butonu
5. İzin ver
```

### C. Render Dashboard

Artık Render Dashboard'dayız! 🎉

---

## 🎯 ADIM 7: WEB SERVICE OLUŞTUR (5 Dakika)

### A. New Web Service

```
1. Render Dashboard
2. "New +" butonu (sağ üstte)
3. "Web Service" seç
```

### B. GitHub Repository Bağla

```
1. "Connect a repository" ekranı
2. Sağ tarafta "Configure account" linki
3. Yeni pencere: Render'a GitHub izinleri
4. "Only select repositories" seç
5. "Kripto-Analiz" reposunu seç
6. "Install" butonu
```

Render Dashboard'a dön:
```
7. "Kripto-Analiz" reposu listede göreceksin
8. "Connect" butonu
```

### C. Web Service Ayarları

**Temel Ayarlar:**
```
Name: whale-alert-bot
   (Otomatik URL olur: https://whale-alert-bot.onrender.com)

Region: Frankfurt
   (Türkiye'ye en yakın)

Branch: main

Runtime: Python 3
   (Otomatik tespit edilir)
```

**Build & Deploy Settings:**
```
Build Command: pip install -r requirements.txt
   (Otomatik doldurulur)

Start Command: bash start.sh
   (Manuel gir)
```

**Instance Type:**
```
Plan: Free
   (750 saat/ay ücretsiz)
```

### D. Environment Variables

⚠️ **EN ÖNEMLİ ADIM!**

"Advanced" butonuna tıkla, aşağı kaydır.

**Environment Variables** bölümünde **"Add Environment Variable"**:

```
Key: TELEGRAM_BOT_TOKEN
Value: 8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw
```

**"Add Environment Variable"** tekrar:
```
Key: TELEGRAM_CHAT_ID
Value: 5893328982
```

**"Add Environment Variable"** tekrar:
```
Key: MIN_VOLUME
Value: 5000
```

**"Add Environment Variable"** son:
```
Key: RENDER
Value: true
```

**Toplam 4 environment variable olmalı!**

### E. Deploy!

```
"Create Web Service" butonu → Deployment başlar! 🚀
```

---

## 🎯 ADIM 8: DEPLOYMENT TAKİBİ (5-10 Dakika)

### A. Build Süreci

```
Render'da "Logs" sekmesi:

1. ==> Cloning from https://github.com/...
2. ==> Downloading cache...
3. ==> Running build command 'pip install -r requirements.txt'...
4. Installing packages...
   ✅ selenium
   ✅ webdriver-manager
   ✅ loguru
   ✅ requests
   (vs. 50+ paket)
5. ==> Build successful!
```

### B. Deploy Süreci

```
6. ==> Deploying...
7. ==> Starting service with 'bash start.sh'...
8. Log'larda göreceksin:
   🐋 Whale Alert Bot başlatılıyor...
   📱 TELEGRAM BİLDİRİMLERİ AKTİF!
   🌐 Sunucu ortamı tespit edildi - Headless mode aktif
   ✅ Chrome başlatıldı
   ✅ Login başarılı
   🚀 CANLI VERİ AKIŞI BAŞLADI
```

### C. Live Durumu

```
Sol üstte durum:
⚫ Building (5 dk)
  ↓
🟡 Deploying (2 dk)
  ↓
🟢 Live (BAŞARILI!) ✅
```

### D. URL'i Kopyala

```
Service URL: https://whale-alert-bot.onrender.com
(Bu URL'i kaydet - uyumama çözümünde lazım)
```

---

## 🎯 ADIM 9: UYUMAMA ÇÖZÜMÜ - UPTIMEROBOT (3 Dakika)

### A. UptimeRobot'a Git

```
https://uptimerobot.com
```

### B. Kayıt Ol

```
1. "Free Sign Up" butonu
2. Email: berkaysnmz1903@gmail.com
3. Password: Güçlü şifre
4. Email doğrulama
```

### C. Monitor Ekle

```
1. Dashboard → "+ Add New Monitor" butonu
2. Ayarlar:

   Monitor Type: HTTP(s)
   
   Friendly Name: Whale Alert Bot
   
   URL (or IP): https://whale-alert-bot.onrender.com
   
   Monitoring Interval: 5 minutes
   (Ücretsiz planda minimum)
   
3. "Create Monitor" butonu
```

### D. Monitor Aktif

```
Dashboard'da göreceksin:
✅ Whale Alert Bot
   Status: Up
   Uptime: 100%
   Response Time: ~200ms
```

**Sonuç:** UptimeRobot her 5 dakikada botu ping atar → Asla uyumaz! 🎉

---

## 🎯 ADIM 10: TEST VE KONTROL (5 Dakika)

### A. Render Logs

```
Render Dashboard → whale-alert-bot → "Logs" tab

Aradaki loglar:
✅ 🔄 Sayfa yenileniyor - Güncel veriler çekiliyor...
✅ ✅ Sayfa yenilendi - Veri akışı devam ediyor
✅ 🚨 WHALE ALERT! - BTCUSDT
✅ ✅ BTCUSDT: Medium Long → Alert gönderildi!
```

### B. Telegram Kontrolü

```
1. Telegram'ı aç
2. Bot'tan mesaj bekle (5-10 dakika)
3. İlk mesaj geldiğinde:
   ✅ BAŞARILI! Bot çalışıyor! 🎉
```

### C. Manuel Test Mesajı

```powershell
# Test mesajı gönder
python -c "import requests; requests.post('https://api.telegram.org/bot8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw/sendMessage', data={'chat_id': '5893328982', 'text': '✅ Render.com sunucusundan test mesajı! Bot aktif 🐋'})"
```

Telegram'da mesaj geldi mi? ✅ BAŞARILI!

---

## 🎉 TAMAMLANDI!

### ✅ Başarı Kontrol Listesi

- [x] Git kuruldu
- [x] GitHub hesabı oluşturuldu
- [x] Personal Access Token oluşturuldu
- [x] GitHub repository oluşturuldu
- [x] Proje GitHub'a push edildi
- [x] Render.com kaydı yapıldı
- [x] Web Service oluşturuldu
- [x] Environment variables ayarlandı
- [x] Bot deploy edildi ve Live durumda
- [x] UptimeRobot eklendi
- [x] Telegram mesajları geliyor

---

## 🌐 SONUÇ

```
✅ Bilgisayarın artık kapalı olabilir
✅ Bot Render.com sunucusunda 24/7 çalışıyor
✅ Telegram'a bildirimler geliyor
✅ UptimeRobot ile asla uyumuyor
✅ Hiçbir ücret yok ($0/ay)
✅ Her yerden erişim (telefon, tablet)
```

---

## 🔄 GÜNCELLEME YAPMAK İSTERSEN

```powershell
# 1. Kod değiştir (örn: whale_alert_bot_v2.py)

# 2. Git komutları
git add .
git commit -m "Bot güncellendi"
git push

# 3. Render otomatik deploy eder!
# 2-3 dakika sonra yeni versiyon çalışır
```

---

## 🐛 SORUN GİDERME

### "Build Failed" Hatası
```
Render Logs → Build hatası mesajını oku
Genelde: requirements.txt eksik paket
Çözüm: Paketi ekle, git push
```

### "Start Command Failed"
```
Render Logs → "bash: start.sh: command not found"
Çözüm:
git update-index --chmod=+x start.sh
git commit -m "Make start.sh executable"
git push
```

### Telegram Mesaj Gelmiyor
```
Render → Settings → Environment Variables kontrol et:
✅ TELEGRAM_BOT_TOKEN doğru mu?
✅ TELEGRAM_CHAT_ID doğru mu?
```

---

**Hazırlayan**: AI Assistant  
**Tarih**: 7 Ekim 2025  
**Durum**: Adım adım rehber - takip et!  
**Süre**: ~30 dakika (ilk kez yapıyorsan)

🚀 Haydi başlayalım! İlk adım: Git kurulumu!
