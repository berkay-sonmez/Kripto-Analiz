# Kripto Analiz Botu - Hızlı Başlangıç Rehberi

## 📋 Gereksinimler

- **Python 3.8 veya üzeri** (Henüz kurulu değil - aşağıdan indirin)
- İnternet bağlantısı
- TradingView hesabı (ücretsiz olabilir)

## 🔧 1. Python Kurulumu

### Windows için:

1. Python'u indirin: https://www.python.org/downloads/
2. İndirdiğiniz dosyayı çalıştırın
3. ⚠️ **ÖNEMLİ**: "Add Python to PATH" seçeneğini işaretleyin!
4. "Install Now" tıklayın

Kurulumdan sonra PowerShell'i **yeniden başlatın** ve şunu test edin:

```powershell
python --version
```

`Python 3.x.x` şeklinde bir çıktı görmelisiniz.

## 🚀 2. Bot Kurulumu

### Adım 1: Virtual Environment Oluştur

```powershell
# Proje klasörüne git
cd "c:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz"

# Virtual environment oluştur
python -m venv .venv

# Aktive et
.\.venv\Scripts\Activate.ps1
```

**Not:** PowerShell script çalıştırma hatası alırsanız:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Adım 2: Bağımlılıkları Yükle

```powershell
# pip'i güncelle
python -m pip install --upgrade pip

# Gerekli paketleri yükle
pip install -r requirements.txt
```

### Adım 3: Yapılandırma

`.env` dosyası oluşturun (`.env.example` dosyasını kopyalayın):

```powershell
Copy-Item .env.example .env
notepad .env
```

`.env` dosyasını düzenleyin:

```env
TRADINGVIEW_USERNAME=sizin_kullanici_adiniz
TRADINGVIEW_PASSWORD=sizin_sifreniz
UPDATE_INTERVAL=300
MIN_VOLUME=1000000
```

## 📊 3. Kullanım

### Test: Altcoin Verilerini Çek

```powershell
python scripts\fetch_coins.py
```

Bu komut:
- 36+ popüler altcoin verisini çeker
- Fiyat, hacim, RSI, MACD verilerini gösterir
- data/ klasörüne JSON ve CSV olarak kaydeder

### Analiz Yap

```powershell
python scripts\analyze.py
```

Bu komut:
- Kaydedilmiş verileri analiz eder
- AL/SAT sinyalleri üretir
- Güçlü fırsatları gösterir

### Ana Botu Çalıştır (Sürekli Çalışma Modu)

```powershell
python main.py
```

Bu komut:
- Her 5 dakikada (300 saniye) verileri günceller
- Otomatik analiz yapar
- Sinyalleri gerçek zamanlı gösterir
- **Durdurmak için:** `Ctrl+C`

## 📁 Klasör Yapısı

```
Kripto-Analiz/
├── .venv/                  # Python virtual environment
├── data/                   # Kaydedilen veriler (JSON, CSV)
├── logs/                   # Bot log dosyaları
├── src/
│   ├── tradingview/       # TradingView API client
│   ├── analyzers/         # Teknik analiz modülleri
│   └── utils/             # Yardımcı fonksiyonlar
├── scripts/               # Hızlı kullanım scriptleri
├── main.py                # Ana bot dosyası
├── requirements.txt       # Python bağımlılıkları
└── .env                   # Yapılandırma (gizli)
```

## 🎯 Özellikler

### Desteklenen Coinler

Bot şu anda 36 popüler altcoin'i izliyor:
- ETH, BNB, XRP, ADA, SOL, DOGE, DOT, MATIC
- LTC, AVAX, LINK, UNI, ATOM, XLM, NEAR
- ALGO, VET, FIL, HBAR, APT, ARB, OP
- SAND, MANA, AXS, IMX, GRT, ENJ, CHZ
- AAVE, MKR, SNX, CRV, COMP, SUSHI, YFI

### Teknik İndikatörler

- **RSI (Relative Strength Index)**: Aşırı alım/satım tespiti
- **MACD**: Trend değişimi sinyalleri
- **Moving Averages**: Destek/direnç seviyeleri
- **Volume Analysis**: Hacim bazlı sinyaller

### Sinyal Tipleri

- 🟢 **BUY (AL)**: Alım fırsatı
- 🔴 **SELL (SAT)**: Satış sinyali
- ⚪ **HOLD (TUT)**: Bekle
- 💪 **STRONG**: Güçlü sinyal (daha yüksek güvenilirlik)

## 🔍 Sorun Giderme

### "Python bulunamadı" hatası

- Python'u yükleyin: https://www.python.org/downloads/
- PATH'e eklendiğinden emin olun
- PowerShell'i yeniden başlatın

### "Execution Policy" hatası

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "ModuleNotFoundError" hatası

```powershell
# Virtual environment'ı aktive edin
.\.venv\Scripts\Activate.ps1

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### TradingView bağlantı hatası

- `.env` dosyasındaki kullanıcı adı ve şifreyi kontrol edin
- TradingView hesabınızın aktif olduğundan emin olun

## 📈 Gelişmiş Kullanım

### Özel Coin Listesi

`src/tradingview/tv_client.py` dosyasındaki `MAJOR_ALTCOINS` listesini düzenleyin.

### Analiz Parametreleri

`src/analyzers/technical_analyzer.py` dosyasında RSI eşiklerini değiştirebilirsiniz:

```python
self.rsi_oversold = 30   # Aşırı satım
self.rsi_overbought = 70 # Aşırı alım
```

### Güncelleme Aralığı

`.env` dosyasında `UPDATE_INTERVAL` değerini saniye cinsinden ayarlayın.

## 🤝 Yardım

Sorunlarınız için:
1. `logs/` klasöründeki log dosyalarını kontrol edin
2. GitHub Issues açın
3. README'yi tekrar okuyun

## ⚠️ Uyarı

Bu bot yalnızca bilgilendirme amaçlıdır. Yatırım tavsiyesi değildir. Kendi araştırmanızı yapın ve risklerinizi yönetin.
