# WhaleHunter Network Analizi

WebSocket'ten veri gelmediği için browser'da manuel kontrol yapmamız gerekiyor.

## 📋 Yapılacaklar Listesi

### Adım 1: Browser'da Network Analizi

1. **Chrome/Edge'i aç**
2. **F12** basarak Developer Tools'u aç
3. **Network** sekmesine git
4. **Filtre**: `WS` (WebSocket) veya `XHR/Fetch` seç
5. **whalehunterapp.com/binance-futures** sayfasına git
6. Giriş yap (berkaysnmz1903@gmail.com)
7. Sayfayı yenile (F5)

### Adım 2: Network İsteklerini İncele

Aşağıdaki bilgileri not edin:

#### WebSocket Bağlantısı
```
URL: wss://whalehunterapp.com/?token=XXXXX
Veya: wss://whalehunterapp.com/socket.io/?EIO=4&transport=websocket
Headers:
  - Cookie: session=...
  - Origin: https://whalehunterapp.com
```

#### XHR/Fetch İstekleri
```
Örnek API endpoint'ler:
- GET https://whalehunterapp.com/api/signals
- GET https://whalehunterapp.com/api/whale-data
- GET https://whalehunterapp.com/api/binance/futures
- POST https://whalehunterapp.com/api/subscribe
```

### Adım 3: WebSocket Mesajlarını İncele

Network > WS > Messages sekmesinde:

```json
// Giden mesaj (client -> server)
{"type": "subscribe", "channel": "binance-futures"}

// Gelen mesaj (server -> client)
{
  "type": "signal",
  "data": {
    "symbol": "BTCUSDT",
    "volume": 1500000,
    ...
  }
}
```

### Adım 4: Cookie/Token Bilgisi

Application > Cookies > whalehunterapp.com:
```
session: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
token: bearer_xxxxx
user_id: 12345
```

## 🔍 Ne Bulacağız?

1. **WebSocket başlatma** için gereken token/header
2. **Subscribe mesajı** formatı (hangi channel'a abone olacağız)
3. **Gelen mesaj** formatı (nasıl parse edeceğiz)
4. Alternatif: **REST API endpoint** (WebSocket yerine polling)

## 📝 Bulduğunuz Bilgileri Buraya Yazın

### WebSocket URL:
```
wss://whalehunterapp.com
```

### Başlatma Mesajı (Subscribe):
```json
// Buraya yapıştırın
```

### Örnek Gelen Mesaj:
```json
// Buraya yapıştırın
```

### Cookie/Header:
```
Cookie: 
Authorization: 
```

## 🚀 Sonraki Adım

Yukarıdaki bilgileri bulduktan sonra, `src/whalehunter/ws_client.py` dosyasını güncelleyeceğiz:

1. Doğru WebSocket URL'i
2. Authentication header/cookie
3. Subscribe mesajı gönderme
4. Mesaj parse etme

---

**YARDIM GEREKİYORSA:**

Eğer browser'da bu adımları yapmakta zorlanıyorsanız, şu alternatifleri deneyebiliriz:

1. **Selenium** ile otomatik browser (sayfa yüklenene kadar bekler, JS çalışır)
2. **Playwright** (daha modern, JavaScript engine)
3. **Başka bir whale tracking servisi** (CoinGlass, CryptoQuant, WhaleAlert)

Hangisini tercih edersiniz?
