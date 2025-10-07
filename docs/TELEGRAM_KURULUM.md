# 📱 TELEGRAM BİLDİRİM KURULUM KILAVUZU

## 🚀 Hızlı Başlangıç (5 Dakika)

### 1️⃣ Telegram Bot Oluştur

1. Telegram'da **@BotFather** ile konuşma başlat
2. `/newbot` komutunu gönder
3. Bot için isim ver (örn: "Whale Alert Bot")
4. Kullanıcı adı ver - **bot** ile bitmeli (örn: "berka_whale_alert_bot")
5. **TOKEN** alacaksınız - güvenli yere not edin!
   ```
   Örnek: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### 2️⃣ Chat ID Bul

1. Yeni bot'unuzla konuşmaya başlayın
2. `/start` yazın
3. Tarayıcınızda şu linke gidin (TOKEN yerine kendi token'inizi yazın):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Çıktıda **"chat"** altında **"id"** numarasını bulun:
   ```json
   "chat": {
     "id": 123456789,  ← BU NUMARA
     "first_name": "Berkay",
     ...
   }
   ```
5. Bu numarayı not edin

### 3️⃣ .env Dosyasını Güncelle

1. Projenizde `.env` dosyasını açın (Kripto-Analiz klasöründe)
2. En alttaki satırları doldurun:
   ```properties
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```
3. Dosyayı kaydedin

### 4️⃣ Botu Başlat

1. Desktop'taki **"🐋 Whale Alert Bot"** kısayoluna tıklayın
   
   VEYA
   
2. PowerShell'de çalıştırın:
   ```powershell
   .venv\Scripts\python.exe scripts\whale_alert_bot_v2.py
   ```

## ✅ Ne Zaman Bildirim Alacaksınız?

### 🚨 MEDIUM Sinyal (2 bip)
- Telefona mesaj:
  ```
  🚨 WHALE ALERT
  
  📍 Coin: BTCUSDT
  📊 Sinyal: Long (Medium)
  💵 Fiyat: 62,345.50
  📈 24h: +2.5%
  💰 Hacim: 1,234,567 USDT
  ```

### 🔥 HIGH Sinyal (8 bip)
- Telefona **kalın** mesaj:
  ```
  🔥🔥🔥 HIGH STRENGTH WHALE! 🔥🔥🔥
  
  📍 Coin: ETHUSDT
  📊 Sinyal: Short (High)
  💵 Fiyat: 3,456.78
  📈 24h: -1.2%
  💰 Hacim: 5,678,901 USDT
  
  💡 HEMEN KONTROL EDİN!
  ```

### 🔥 TEKRAR SİNYAL (10 bip)
- Aynı coinde 1 saat içinde 2+ sinyal:
  ```
  🔥🔥 TEKRAR SİNYAL! 🔥🔥
  
  📍 Coin: SOLUSDT
  🔢 Son 1 saat: 3 SİNYAL!
  🎯 Yön: 📈 LONG DOMINANT (2L / 1S)
  💵 Son Fiyat: 145.67
  💰 Son Hacim: 987,654 USDT
  
  💡 YOĞUN AKTİVİTE - ÖNCELİK VERİN!
  ```

## 🔧 Sorun Giderme

### ❌ "Telegram bildirimleri kapalı" mesajı
- `.env` dosyasında `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` boş olabilir
- Değerleri kontrol edin, boşluk bırakmayın:
  ```properties
  TELEGRAM_BOT_TOKEN=123456789:ABCdefGHI...
  TELEGRAM_CHAT_ID=123456789
  ```

### ❌ Bot çalışıyor ama mesaj gelmiyor
1. **Bot'a /start yazdınız mı?** Bot'unuzla konuşma başlatmadan mesaj gelmez!
2. **Chat ID doğru mu?** `getUpdates` linkinden tekrar kontrol edin
3. **Token doğru mu?** @BotFather'a `/mybots` yazıp token'i yeniden alabilirsiniz

### ❌ "Unauthorized" hatası
- Token yanlış veya eksik. @BotFather'dan yeni token alın

### ❌ "Chat not found" hatası
- Chat ID yanlış. Bot'a `/start` yazın ve `getUpdates` ile tekrar kontrol edin

## 📱 Telegram Mesaj Ayarları

### Bildirimleri Sessiz Al
1. Bot'la konuşmanın üstüne tıklayın (üç nokta)
2. "Bildirimler" → "Sessiz"

### Sadece Önemli Olanları Al
Kod'u düzenleyerek sadece HIGH sinyalleri alabilirsiniz:
```python
# whale_alert_bot_v2.py içinde
# MEDIUM mesajları kaldır:
# self.send_telegram_message(telegram_msg)  # Bu satırı # ile başlat
```

## 🎯 İpuçları

1. **7/24 Çalıştırın**: Bilgisayarınız açıkken bot sürekli çalışır
2. **Telefonunuzu Sessizde Bırakmayın**: Gece bildirimleri almak isterseniz
3. **Coin Sembolüne Tıklayın**: Telegram'da coin sembolü tıklanabilir olmasa da kopyalayıp trading platformuna yapıştırabilirsiniz
4. **Geçmiş Mesajları Takip**: Telegram'da tüm geçmiş sinyaller kalır

## 🔒 Güvenlik

- **Token'i kimseyle paylaşmayın!** Herkes bu token ile sizin adınıza mesaj gönderebilir
- `.env` dosyasını GitHub'a yüklemeyin (zaten `.gitignore`'da var)
- Token sızdıysa: @BotFather → `/mybots` → Botunuz → "API Token" → "Revoke" → Yeni token alın

## ✅ Test Et!

Bot çalışırken bir sinyal geldiğinde hem:
- 🖥️ Konsolda görürsünüz
- 🔊 Ses duyarsınız  
- 📱 Telegram'dan bildirim alırsınız

İyi işlemler! 🚀
