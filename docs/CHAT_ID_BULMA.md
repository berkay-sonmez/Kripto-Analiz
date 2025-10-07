# 📱 TELEGRAM CHAT ID BULMA KILAVUZU

## Yöntem 1: Otomatik Script (ÖNERİLEN)

### Adım 1: Bot Token Alın

1. Telegram'da **@BotFather** ile konuşun
2. Komutlar:
   - Yeni bot: `/newbot`
   - Var olan bot: `/mybots` → Botunuz → "API Token"
3. Token'i kopyalayın:
   ```
   Örnek: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### Adım 2: Bot'a Mesaj Gönderin

1. Kendi bot'unuza gidin
2. `/start` yazın ve gönder

### Adım 3: Script Çalıştır

PowerShell'de:
```powershell
.venv\Scripts\python.exe scripts\find_telegram_chat_id.py
```

Token'i yapıştırın (SADECE TOKEN, URL değil!)

### Sonuç:
```
✅ CHAT ID BULUNDU!

==================================================
📍 Chat ID: 123456789
👤 İsim: Berkay
==================================================

📋 .env dosyasına ekleyin:
   TELEGRAM_CHAT_ID=123456789
```

---

## Yöntem 2: Manuel (Tarayıcı)

### Adım 1: Token Hazırla

@BotFather'dan token'i al (yukarıdaki gibi)

### Adım 2: Bot'a Mesaj Gönder

Bot'a `/start` yaz

### Adım 3: Tarayıcıda Aç

Bu linki açın (TOKEN yerine kendi token'inizi yazın):
```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

Örnek:
```
https://api.telegram.org/bot123456789:ABCdefGHI/getUpdates
```

### Adım 4: Chat ID Bul

Çıktıda şöyle bir bölüm göreceksiniz:
```json
{
  "ok": true,
  "result": [
    {
      "message": {
        "chat": {
          "id": 123456789,  ← BU NUMARA!
          "first_name": "Berkay",
          "type": "private"
        }
      }
    }
  ]
}
```

**"id"** değerini kopyalayın.

---

## Yöntem 3: Telegram'dan Direkt

1. Telegram Desktop veya Web (https://web.telegram.org) açın
2. **userinfobot** kullanın:
   - @userinfobot ile konuşma başlatın
   - `/start` yazın
   - Size Chat ID'nizi verecek

---

## ✅ Son Adım: .env Dosyasını Güncelle

1. `.env` dosyasını açın
2. Son satırlara ekleyin:
   ```properties
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=123456789
   ```
3. Kaydet

---

## 🧪 Test Et

Bot'u başlatın:
```powershell
.venv\Scripts\python.exe scripts\whale_alert_bot_v2.py
```

Başlangıçta göreceksiniz:
```
📱 TELEGRAM BİLDİRİMLERİ AKTİF!
```

Bir sinyal geldiğinde telefonunuza mesaj gelecek! 🎉
