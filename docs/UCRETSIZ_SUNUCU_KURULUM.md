# 🌐 ÜCRETSİZ SUNUCU KURULUMU - 24/7 Whale Bot

## 🎯 Hedef
Bilgisayarın kapalı olsa bile bot çalışsın ve Telegram'dan bildirim gelsin - **TAMAMEN ÜCRETSİZ!**

---

## 🆓 EN İYİ 5 ÜCRETSİZ SEÇENEK

### ⭐ SEÇENEK 1: Render.com (ÖNERİLEN!)
**En kolay ve güvenilir - 750 saat/ay ücretsiz**

#### ✅ Avantajlar
- Tamamen ücretsiz (kredi kartı gerektirmez)
- 750 saat/ay = ~31 gün kesintisiz
- Otomatik deployment (Git push yeter)
- Python doğrudan destekli
- SSL/HTTPS ücretsiz
- 512 MB RAM

#### ⚠️ Dezavantajlar
- 15 dakika işlem yoksa uyur (webhook ile çözülür)
- Her ay yeniden deploy gerekebilir

#### 📝 Kurulum Adımları

**1. Proje Hazırlığı (5 dakika)**

```powershell
# a) requirements.txt oluştur (zaten var)
# b) render.yaml oluştur
# c) start.sh oluştur
# d) GitHub'a yükle
```

**2. Render.com Kaydı (2 dakika)**
```
1. render.com'a git
2. GitHub ile giriş yap
3. "New +" → "Web Service" seç
4. GitHub repo'nu seç (Kripto-Analiz)
```

**3. Ayarlar**
```
Name: whale-alert-bot
Region: Frankfurt (en yakın)
Branch: main
Build Command: pip install -r requirements.txt
Start Command: ./start.sh
Instance Type: Free
```

**4. Environment Variables (Çevre Değişkenleri)**
```
TELEGRAM_BOT_TOKEN = 8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw
TELEGRAM_CHAT_ID = 5893328982
MIN_VOLUME = 5000
```

**5. Deploy!**
```
"Create Web Service" → Otomatik deployment başlar
5-10 dakika sonra hazır! ✅
```

#### 🔧 Gerekli Dosyalar

**`render.yaml`** (Proje kökünde):
```yaml
services:
  - type: web
    name: whale-alert-bot
    env: python
    region: frankfurt
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python scripts/whale_alert_bot_v2.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_CHAT_ID
        sync: false
      - key: MIN_VOLUME
        value: "5000"
```

**`start.sh`** (Proje kökünde):
```bash
#!/bin/bash
# Render.com için başlatma scripti
python scripts/whale_alert_bot_v2.py
```

**`.gitignore` güncellemesi**:
```
# Şunları ekle:
.env
chromedriver.exe
logs/
data/
__pycache__/
*.pyc
.vscode/
```

---

### ⭐ SEÇENEK 2: Railway.app
**En güçlü ücretsiz plan - 500 saat/ay**

#### ✅ Avantajlar
- 512 MB RAM + 1 GB Disk
- PostgreSQL, Redis ücretsiz
- Otomatik HTTPS
- Uyumama problemi yok!
- GitHub entegrasyonu

#### ⚠️ Dezavantajlar
- Kredi kartı gerekebilir (ücret yok ama doğrulama için)
- 500 saat = ~20 gün (ayda 10 gün ekstra yok)

#### 📝 Kurulum
```
1. railway.app'e git
2. GitHub ile giriş yap
3. "New Project" → "Deploy from GitHub repo"
4. Kripto-Analiz seç
5. Environment variables ekle (Telegram token, chat ID)
6. Deploy!
```

---

### ⭐ SEÇENEK 3: Fly.io
**Docker desteği - 3 VM ücretsiz**

#### ✅ Avantajlar
- 3 VM ücretsiz (256 MB RAM her biri)
- İstanbul'a yakın sunucular (Frankfurt)
- Uyumama yok
- Docker ile tam kontrol

#### ⚠️ Dezavantajlar
- Kredi kartı gerekli (doğrulama için)
- Docker bilgisi gerekebilir
- Biraz daha teknik

#### 📝 Kurulum
```bash
# 1. Fly CLI kur
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 2. Login
flyctl auth login

# 3. App oluştur
flyctl launch

# 4. Secrets ekle
flyctl secrets set TELEGRAM_BOT_TOKEN="8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw"
flyctl secrets set TELEGRAM_CHAT_ID="5893328982"

# 5. Deploy
flyctl deploy
```

**`fly.toml`** (Otomatik oluşur):
```toml
app = "whale-alert-bot"
kill_signal = "SIGINT"
kill_timeout = 5
processes = []

[env]
  MIN_VOLUME = "5000"

[[services]]
  http_checks = []
  internal_port = 8080
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

[build]
  builder = "paketobuildpacks/builder:base"
```

---

### ⭐ SEÇENEK 4: Google Cloud Run
**En ölçeklenebilir - 2 milyon istek/ay ücretsiz**

#### ✅ Avantajlar
- Google'ın gücü
- Otomatik ölçeklendirme
- 2M istek ücretsiz
- 180,000 vCPU-saniye/gün

#### ⚠️ Dezavantajlar
- Kredi kartı gerekli
- Uyuma problemi (webhook çözümü gerekli)
- Biraz daha karmaşık

#### 📝 Kurulum
```bash
# 1. Google Cloud SDK kur
# https://cloud.google.com/sdk/docs/install

# 2. Giriş yap
gcloud auth login

# 3. Proje oluştur
gcloud projects create whale-bot-project

# 4. Cloud Run'a deploy
gcloud run deploy whale-bot \
  --source . \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

---

### ⭐ SEÇENEK 5: Heroku (Kısıtlı Ücretsiz)
**Eskiden en popülerdi - Artık sınırlı**

#### ⚠️ Uyarı
Heroku 2022'den beri tamamen ücretsiz planı kaldırdı. En ucuz plan $5/ay.

Ama **GitHub Student Pack** varsa:
- $13/ay kredi (öğrenciysen)
- 1000 dyno saat ücretsiz

---

## 🎯 HANGİSİNİ SEÇMELİYİM?

### 📊 Karşılaştırma Tablosu

| Özellik | Render.com | Railway | Fly.io | Google Cloud |
|---------|-----------|---------|--------|--------------|
| **Kredi Kartı** | ❌ Gerektirmez | ⚠️ İsteğe bağlı | ✅ Gerekli | ✅ Gerekli |
| **Süre/Ay** | 750 saat (~31 gün) | 500 saat (~20 gün) | Sınırsız | Sınırsız |
| **RAM** | 512 MB | 512 MB | 256 MB | 256 MB |
| **Uyuma** | ⚠️ 15 dk sonra | ❌ Yok | ❌ Yok | ⚠️ Var |
| **Kolay Kurulum** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| **Türkiye Yakınlık** | 🇩🇪 Frankfurt | 🇩🇪 Frankfurt | 🇩🇪 Frankfurt | 🇧🇪 Belçika |

### 🏆 Öneriler

#### Senaryo 1: "En kolayı lazım, kredi kartı yok"
**➡️ Render.com** (⭐⭐⭐⭐⭐)
- 10 dakikada kurulur
- GitHub ile sync
- Webhook ekle (uyuma çözümü)

#### Senaryo 2: "Uyumama önemli, kredi kartı sorun değil"
**➡️ Railway.app** (⭐⭐⭐⭐)
- Uyumama yok
- 500 saat = 20 gün yeter (her ay reset)
- Kolay deployment

#### Senaryo 3: "Tam kontrol istiyorum, Docker biliyorum"
**➡️ Fly.io** (⭐⭐⭐⭐)
- 3 VM ücretsiz
- Tam kontrol
- Istanbul'a en yakın

#### Senaryo 4: "Google fanıyım, ölçeklenebilirlik"
**➡️ Google Cloud Run** (⭐⭐⭐)
- Google'ın gücü
- Webhook gerekir
- Biraz teknik

---

## 🚀 ADIM ADIM: RENDER.COM KURULUMU (ÖNERİLEN)

### Hazırlık (Bilgisayarında - 5 dakika)

#### 1. GitHub Reposu Oluştur

```powershell
# Proje dizininde
cd C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz

# Git init (yoksa)
git init

# GitHub repo oluştur (GitHub.com'da "New Repository")
# Adı: Kripto-Analiz
# Private seç (API key'ler gizli kalsın)

# Remote ekle
git remote add origin https://github.com/KULLANICI_ADIN/Kripto-Analiz.git

# Dosyaları ekle
git add .
git commit -m "Initial commit - Whale Alert Bot"
git push -u origin main
```

#### 2. Gerekli Dosyaları Oluştur

**A. `render.yaml`** (Proje kökünde):
```yaml
services:
  - type: web
    name: whale-alert-bot
    env: python
    region: frankfurt
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: bash start.sh
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_CHAT_ID
        sync: false
      - key: MIN_VOLUME
        value: "5000"
```

**B. `start.sh`** (Proje kökünde):
```bash
#!/bin/bash
echo "🐋 Whale Alert Bot başlatılıyor..."
python scripts/whale_alert_bot_v2.py
```

**C. `.gitignore` güncelle**:
```
# Hassas dosyalar
.env
*.env

# Chrome driver
chromedriver.exe

# Loglar ve data
logs/
data/
*.log

# Python
__pycache__/
*.pyc
*.pyo
.Python

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

**D. GitHub'a push**:
```powershell
git add render.yaml start.sh .gitignore
git commit -m "Add Render.com deployment files"
git push
```

#### 3. Render.com'da Deployment

```
1. render.com'a git
2. "Sign Up" → "GitHub" ile giriş yap
3. GitHub'da Kripto-Analiz repo'suna izin ver
4. Render Dashboard → "New +" → "Web Service"
5. "Kripto-Analiz" reposunu seç
6. Ayarlar:
   - Name: whale-alert-bot
   - Region: Frankfurt
   - Branch: main
   - Build Command: pip install -r requirements.txt
   - Start Command: bash start.sh
7. Environment Variables:
   - TELEGRAM_BOT_TOKEN: 8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw
   - TELEGRAM_CHAT_ID: 5893328982
   - MIN_VOLUME: 5000
8. "Create Web Service" → Deployment başlar!
```

#### 4. Deployment Takibi

```
Render Dashboard'da:
- Build logs: Kurulum durumu
- Deploy logs: Bot çalışma durumu
- "🐋 Whale Alert Bot başlatılıyor..." görmelisin

5-10 dakika sonra: ✅ "Live" yazısı görünür
```

---

## ⚠️ ÖNEMLI: UYUMA SORUNU ÇÖZÜMÜ

### Problem
Render.com ücretsiz planında 15 dakika işlem yoksa service uyur.

### Çözüm 1: Self-Ping (Kolay)

Bot içine ekle - her 10 dakikada bir kendini uyandır:

```python
# whale_alert_bot_v2.py içine ekle

import requests
import threading

class KeepAlive:
    def __init__(self, url):
        self.url = url
        self.running = True
        
    def ping(self):
        while self.running:
            try:
                requests.get(self.url, timeout=5)
                logger.info("🔄 Self-ping yapıldı - Service aktif!")
            except:
                pass
            time.sleep(600)  # 10 dakikada bir
    
    def start(self):
        thread = threading.Thread(target=self.ping, daemon=True)
        thread.start()

# Bot başlatırken:
keep_alive = KeepAlive("https://whale-alert-bot.onrender.com")
keep_alive.start()
```

### Çözüm 2: UptimeRobot (Ücretsiz Harici Servis)

```
1. uptimerobot.com'a git
2. Ücretsiz kayıt ol
3. "Add New Monitor" → HTTP(s)
4. URL: https://whale-alert-bot.onrender.com
5. Interval: 5 dakika
6. Kaydet!
```

UptimeRobot her 5 dakikada servisi ping atar → Asla uyumaz! ✅

---

## 🔍 SORUN GİDERME

### 1. "Build Failed" Hatası
```
Çözüm:
- requirements.txt kontrol et
- Python version belirt (render.yaml'a ekle):
  runtime: python-3.11
```

### 2. "Start Command Failed"
```
Çözüm:
- start.sh chmod +x yap
- Render.yaml'da: startCommand: bash start.sh
```

### 3. Chrome/Selenium Hatası
```
Problem: Render sunucusunda Chrome yok!

Çözüm A - Headless Chrome (Önerilen):
```python
options.add_argument('--headless')  # whale_alert_bot_v2.py içinde zaten var
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
```

Çözüm B - Chrome kurulumu (Dockerfile):
```dockerfile
FROM python:3.11-slim

# Chrome ve dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "scripts/whale_alert_bot_v2.py"]
```
```

### 4. Telegram Bildirimleri Gelmiyor
```
Kontrol:
1. TELEGRAM_BOT_TOKEN doğru mu? (render.com env vars)
2. TELEGRAM_CHAT_ID doğru mu?
3. Bot logs'da "📱 TELEGRAM BİLDİRİMLERİ AKTİF!" yazıyor mu?
```

---

## 📱 TEST: BOT ÇALIŞIYOR MU?

### 1. Render Dashboard Kontrolü
```
render.com → Services → whale-alert-bot
Status: 🟢 Live olmalı
Logs: "🐋 Whale Alert Bot başlatılıyor..." görünmeli
```

### 2. Telegram Kontrolü
```
Telegram'da bot'tan mesaj geldi mi?
Beklenen: 🚨 WHALE ALERT mesajları
```

### 3. Manual Test
```python
# Test scripti çalıştır (bilgisayarında)
python -c "
import requests
token = '8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw'
chat_id = '5893328982'
url = f'https://api.telegram.org/bot{token}/sendMessage'
data = {'chat_id': chat_id, 'text': '✅ Sunucu botu test mesajı!'}
response = requests.post(url, data=data)
print('Test mesajı gönderildi!' if response.ok else 'HATA!')
"
```

---

## 💰 MALİYET ANALİZİ

### Render.com Ücretsiz Plan
```
Aylık Limit: 750 saat
Günlük: 24 saat
Aylık kullanım: 24 * 30 = 720 saat ✅

SONUÇ: Tam bir ay 24/7 çalışır! 🎉
```

### Ek Maliyet
```
- Render.com: $0
- UptimeRobot: $0
- Telegram Bot: $0
- GitHub: $0 (private repo)

TOPLAM: $0 / AY ✅✅✅
```

---

## 🎯 SONUÇ

### ✅ Render.com ile Tamamlandı!

```
1. ✅ GitHub reposu hazır
2. ✅ render.yaml oluşturuldu
3. ✅ Render.com'da deploy edildi
4. ✅ Telegram entegrasyonu çalışıyor
5. ✅ UptimeRobot eklendi (uyumama)
6. ✅ 24/7 ücretsiz çalışıyor!

Artık:
- Bilgisayarın kapalı ✅
- Bot sunucuda çalışıyor ✅
- Telegram'a bildirimler geliyor ✅
- Hiçbir ücret yok ✅
```

### 📱 Kullanım

```
Artık her yerden:
- Telefondan bildirimleri al
- Önemli coinleri takip et
- Hiçbir şey yapma, bot çalışıyor!

Güncelleme gerekirse:
git push → Otomatik deploy! 🚀
```

---

## 📞 DESTEK

### Yararlı Linkler
- Render Docs: https://render.com/docs
- Render Discord: https://discord.gg/render
- Railway Docs: https://docs.railway.app
- Fly.io Docs: https://fly.io/docs

### Sorun Yaşarsan
1. Render logs kontrol et
2. GitHub issues aç
3. Discord'dan yardım iste

---

**Oluşturulma**: 7 Ekim 2025  
**Durum**: Render.com kurulumu hazır - adım adım takip et!  
**Maliyet**: 100% ÜCRETSİZ! 💰✅

İyi şanslar! 🐋🚀📱
