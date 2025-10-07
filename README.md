# Kripto Analiz Botu

Çoklu veri kaynağı (TradingView, WhaleHunter, Binance) ile altcoin analizi yapan otomatik bot.

## ✨ Özellikler

### 📊 Veri Kaynakları
- **TradingView API**: 36+ altcoin teknik analizi
- **WhaleHunter WebSocket**: Gerçek zamanlı whale (balina) hareketi takibi
- **Binance API**: Canlı fiyat ve hacim verileri

### 🔬 Teknik Analiz
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Moving Averages (EMA, SMA)
- Volume Analysis

### 🐋 Whale Tracking
- Büyük hacimli alım/satım tespiti
- Sinyal gücü analizi (Low/Medium/High)
- LONG/SHORT pozisyon takibi
- Gerçek zamanlı bildirimler

### 📈 Sinyal Üretimi
- BUY/SELL/HOLD önerileri
- Güç seviyesi (STRONG/WEAK/NEUTRAL)
- Detaylı sebep açıklamaları

## Kurulum

```powershell
# Virtual environment oluştur
python -m venv .venv

# Aktive et
.\.venv\Scripts\Activate.ps1

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## Yapılandırma

`.env` dosyası oluşturun:

```env
# TradingView
TRADINGVIEW_USERNAME=kullanici_adi
TRADINGVIEW_PASSWORD=sifre

# WhaleHunter (opsiyonel - whale tracking için)
WHALEHUNTER_EMAIL=email@example.com
WHALEHUNTER_PASSWORD=sifre

# Bot Ayarları
UPDATE_INTERVAL=300  # 5 dakika
MIN_VOLUME=1000000   # Minimum hacim (USDT)
```

## 🚀 Hızlı Başlangıç

### TradingView Analizi
```powershell
# Watchlist'teki coinleri çek (rate-limit-safe)
python scripts\fetch_watchlist_slow.py

# Kaydedilmiş verileri analiz et
python scripts\analyze_saved.py
```

### WhaleHunter Tracking
```powershell
# 🚨 CANLI WHALE ALERT BOT (ÖNERİLEN) - 24/7 İZLEME
# High/Medium sinyallerde ses + bildirim
python scripts\whale_alert_bot.py

# 🎯 HIZLI BAŞLATMA (Arka planda sürekli çalışır)
# Çift tıkla - terminal kapatılabilir
start_whale_bot.bat

# Tek seferlik veri çekme (60 saniye)
python scripts\selenium_whalehunter.py

# WebSocket test (gelişmiş)
python scripts\test_websocket.py
```

### 🔥 Kalıcı Arka Plan Çalışma

Bot'un **bilgisayar kapanana kadar** çalışması için:

1. **Hızlı Başlatma**: Çift tıkla `start_whale_bot.bat`
2. **Otomatik Başlangıç**: `docs\KALICI_ARKAPLAN_KILAVUZU.md` oku
3. **Task Scheduler**: Windows servisi gibi çalışır

📚 Detaylı kılavuz: `docs\KALICI_ARKAPLAN_KILAVUZU.md`

### Binance API
```powershell
# Binance'den anlık veri çek
python scripts\analyze_binance.py
```

### Komple Bot
```powershell
# Sürekli çalışan bot (tüm kaynaklar)
python main.py
```

## 📋 Watchlist Yönetimi

`src/config/my_watchlist.py` dosyasında coin listesini düzenleyin:

```python
MY_WATCHLIST = [
    "BTC", "ETH", "BNB", "SOL",
    # Kendi coinlerinizi ekleyin
]
```

## 📁 Proje Yapısı

```
├── src/
│   ├── tradingview/      # TradingView API client
│   │   └── tv_client.py
│   ├── whalehunter/      # WhaleHunter WebSocket client
│   │   ├── wh_client.py  # HTTP scraper
│   │   └── ws_client.py  # WebSocket listener
│   ├── binance/          # Binance API client
│   │   └── binance_client.py
│   ├── analyzers/        # Teknik analiz modülleri
│   │   └── technical_analyzer.py
│   ├── config/           # Yapılandırma
│   │   └── my_watchlist.py
│   └── utils/            # Yardımcı fonksiyonlar
│       └── data_manager.py
├── scripts/              # CLI scriptleri
│   ├── fetch_watchlist_slow.py   # TradingView (rate-limit-safe)
│   ├── test_websocket.py         # WhaleHunter WebSocket test
│   ├── analyze_binance.py        # Binance analizi
│   └── analyze_saved.py          # Cached data analizi
├── data/                 # Veri depolama (JSON/CSV)
├── notebooks/            # Jupyter analiz defterleri
└── .env                  # Credentials (git'e eklenmez)
```

## 🔧 Sorun Giderme

### TradingView Rate Limit (429 Error)
- `fetch_watchlist_slow.py` kullanın (3 sn gecikme)
- Alternatif: `analyze_saved.py` ile cached data analiz edin
- Veya WhaleHunter/Binance API kullanın

### WhaleHunter Veri Gelmiyor
- `.env` dosyasında `WHALEHUNTER_EMAIL` ve `WHALEHUNTER_PASSWORD` kontrol edin
- `test_websocket.py` ile bağlantıyı test edin
- Whale sinyalleri gerçek zamanlıdır, beklemek gerekebilir

### Binance SSL Hatası
- Internet bağlantısını kontrol edin
- VPN kullanıyorsanız kapatıp deneyin
- `analyze_binance.py` yerine TradingView kullanın

## 📊 Veri Formatı

### TradingView Response
```json
{
  "symbol": "BTCUSDT",
  "price": 28500.50,
  "rsi": 56.7,
  "recommendation": "BUY",
  "indicators": {...}
}
```

### WhaleHunter Signal
```json
{
  "symbol": "BTCUSDT",
  "signal_type": "LONG",
  "signal_strength": 12.5,
  "volume_usdt": 1500000,
  "strength_label": "High"
}
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit edin (`git commit -m 'feat: Add AmazingFeature'`)
4. Push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın.
