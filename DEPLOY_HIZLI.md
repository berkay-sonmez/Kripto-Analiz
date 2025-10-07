# 🚀 SUNUCUYA YÜKLEME - HIZLI KOMUTLAR

## ⚡ 3 ADIMDA DEPLOY!

### 1️⃣ GitHub'a Yükle (2 Dakika)

```powershell
# Proje dizinine git
cd C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz

# Git init
git init
git add .
git commit -m "Initial commit - Whale Alert Bot"

# GitHub'a bağlan (KULLANICI_ADIN değiştir!)
git remote add origin https://github.com/KULLANICI_ADIN/Kripto-Analiz.git
git branch -M main
git push -u origin main
```

**Not**: GitHub kullanıcı adı ve Personal Access Token gerekir
- Token oluştur: https://github.com/settings/tokens

---

### 2️⃣ Render.com'da Deploy (5 Dakika)

1. **https://render.com** → GitHub ile giriş yap
2. **"New +" → "Web Service"**
3. **Kripto-Analiz** reposunu seç
4. **Ayarlar**:
   ```
   Name: whale-alert-bot
   Region: Frankfurt
   Branch: main
   Build: pip install -r requirements.txt
   Start: bash start.sh
   Instance: Free
   ```
5. **Environment Variables** ekle:
   ```
   TELEGRAM_BOT_TOKEN = 8442539862:AAGTFGBYBm_wLjHh4qJG0PhmsYPglEv-8bw
   TELEGRAM_CHAT_ID = 5893328982
   MIN_VOLUME = 5000
   RENDER = true
   ```
6. **"Create Web Service"** → Deploy başlar! 🚀

---

### 3️⃣ Uyumama Çözümü (2 Dakika)

**UptimeRobot ile:**
1. **https://uptimerobot.com** → Kayıt ol
2. **"Add New Monitor"**:
   ```
   Type: HTTP(s)
   URL: https://whale-alert-bot.onrender.com
   Interval: 5 minutes
   ```
3. **Create!** ✅

---

## ✅ TAMAMLANDI!

Bot artık 24/7 çalışıyor! 🎉

### Kontrol:
- ✅ Render Dashboard → "Live" yazısı
- ✅ Telegram'da mesajlar geliyor
- ✅ Bilgisayarı kapatabilirsin

---

## 🔄 Güncelleme (30 Saniye)

```powershell
# Kod değiştir, sonra:
git add .
git commit -m "Güncelleme"
git push

# Render otomatik deploy eder! 🚀
```

---

## 📱 Sonuç

```
💻 Bilgisayar: Kapalı olabilir
🌐 Bot: Sunucuda çalışıyor
📱 Bildirimler: Telegram'a geliyor
💰 Maliyet: $0/ay - Ücretsiz!
```

🐋 Artık her yerden whale sinyallerini takip edebilirsin!
