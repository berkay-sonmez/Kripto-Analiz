# 🐋 Whale Alert Bot - Kullanım Kılavuzu

## 📋 Genel Bakış

Whale Alert Bot, WhaleHunter'dan gelen büyük hacimli alım/satım sinyallerini takip eder ve sizi **ses + konsol bildirimiyle** uyarır.

## 🎯 Ne Zaman Alert Gelir?

### 1️⃣ HIGH Strength Sinyal (⚡ Anında Alert)
- Herhangi bir coinde **High** sinyal geldiğinde
- 3 kez bip sesi
- Konsola detaylı bilgi

**Örnek:**
```
Symbol: BTCUSDT
Sinyal: LONG (High)
Hacim: $5,000,000
Sebep: ⚡ HIGH STRENGTH SİNYAL!
```

### 2️⃣ MEDIUM Sinyal Üst Üste (🔥 2-3 Kez)
- Aynı coinde aynı yönde (LONG/SHORT) **2-3 Medium** sinyal geldiğinde
- 2 kez bip sesi
- Pattern tespit edildi anlamına gelir

**Örnek:**
```
Symbol: ETHUSDT
Sinyal: SHORT (Medium)
Sebep: 🔥 3 MEDIUM SHORT SİNYALİ ÜST ÜSTE!
```

### 3️⃣ Watchlist Coinleri (📋 Özel Takip)
- `src/config/my_watchlist.py` dosyasındaki coinleriniz
- Bu coinlerde **Medium** sinyal bile geldiğinde alert
- Kendi portföyünüzü takip etmek için

**Örnek:**
```
Symbol: SOLUSDT (Watchlist)
Sinyal: LONG (Medium)
Sebep: 📋 WATCHLİST COİN: LONG Medium sinyal
```

## 🚀 Kullanım

### Basit Kullanım (60 Dakika)
```powershell
# Varsayılan: 60 dakika izleme
python scripts\whale_alert_bot.py
```

### Süresiz İzleme
Kod içinde `duration_minutes=0` yapın:
```python
bot.monitor_whales(duration_minutes=0)  # Sonsuz
```

### Watchlist Düzenleme
`src/config/my_watchlist.py` dosyasını düzenleyin:
```python
MY_WATCHLIST = [
    "BTC", "ETH", "SOL",  # Kendi coinlerinizi ekleyin
]
```

## 🔊 Ses Bildirimleri

| Güç | Bip Sayısı | Frekans |
|-----|-----------|---------|
| High | 3x | 1000Hz |
| Medium | 2x | 800Hz |
| Low | 1x | 600Hz |

**Not:** Windows `winsound` kullanır. Ses gelmiyor mu? Hoparlör kontrolü yapın.

## 📊 Konsol Çıktısı

Alert geldiğinde şu formatta bilgi görürsünüz:

```
======================================================================
🚨 WHALE ALERT! 🚨
======================================================================
⏰ Zaman: 2025-10-05 18:45:30
📍 Coin: BTCUSDT
📊 Sinyal: LONG (High)
💵 Fiyat: 28500.50
📈 24h Değişim: +2.5%
💰 Hacim: $5,123,456 USDT
🎯 Sebep: ⚡ HIGH STRENGTH SİNYAL!
======================================================================
💡 İŞLEM ÖNERİSİ: Bu coini kontrol edin ve işlem açmayı düşünün!
======================================================================
```

## ⚙️ Gelişmiş Ayarlar

### Alert Sıklığını Azaltma
Çok fazla alert geliyorsa, `check_signal_pattern()` fonksiyonunda filtreleri sıkılaştırın:

```python
# Medium için 3 kez zorunlu tut (varsayılan: 2)
if len(same_direction_mediums) >= 2:  # 2 eski + 1 yeni = 3 toplam
    self.send_alert(...)
```

### Sadece Watchlist
Watchlist dışındaki coinleri görmezden gelin:

```python
# check_signal_pattern() başına ekleyin:
if symbol not in self.watchlist_symbols:
    return False  # Watchlist dışı coinleri atla
```

### Minimum Hacim Filtresi
Küçük hacimleri filtreleyin:

```python
# check_signal_pattern() içinde:
volume = float(new_signal['total_usdt'].replace(',', ''))
if volume < 100000:  # 100k USDT altı atla
    return False
```

## 🐛 Sorun Giderme

### Ses Gelmiyor
```python
# Test için:
import winsound
winsound.Beep(1000, 500)  # 1000Hz, 500ms
```

Çalışmıyorsa:
- Hoparlör kontrolü
- Windows ses ayarları
- `winsound` yerine `playsound` kullanın

### Alert Gelmiyor
1. Watchlist coinlerinizi kontrol edin
2. Piyasa sessiz olabilir (whale hareketi yok)
3. Console'da `logger.debug` mesajlarını açın:
   ```python
   logger.remove()
   logger.add(sys.stderr, level="DEBUG")
   ```

### Browser Kapanıyor
Login sorunuysa:
- `.env` dosyasında email/password kontrol edin
- WhaleHunter hesabınız aktif mi?

## 📈 Kullanım Stratejisi

### 1. Sabah Rutin (09:00-10:00)
```powershell
# 60 dakika izle, kahvaltı yaparken
python scripts\whale_alert_bot.py
```

### 2. Öğlen Kontrolü (12:00-13:00)
```powershell
# Kısa 30 dakikalık check
# duration_minutes=30 yap
```

### 3. Akşam Volatilite (20:00-22:00)
```powershell
# Amerikan piyasası açılışı
# 2 saat izle (duration_minutes=120)
```

### 4. 7/24 İzleme
```powershell
# VPS veya bulut sunucuda sürekli çalıştır
# duration_minutes=0 (sonsuz)
# & (arka planda) veya screen/tmux kullan
```

## 💡 Pro İpuçları

1. **Watchlist = Portföy**: Elinizdeki coinleri ekleyin
2. **High Alert = Acil**: High gelirse hemen grafiği kontrol edin
3. **3x Medium = Trend**: Üst üste Medium'lar trend gösterir
4. **Hacim > Güç**: Düşük güç + büyük hacim = dikkat
5. **Bildirim + Manuel Analiz**: Alert gelince TradingView'da teknik analiz yapın

## 🔄 Otomatik Başlatma (Windows)

Task Scheduler ile otomatik başlatma:

1. Task Scheduler'ı aç
2. "Create Basic Task"
3. Trigger: "When I log on" veya "Daily at 09:00"
4. Action: "Start a program"
5. Program: `C:\Users\...\python.exe`
6. Arguments: `C:\Users\...\whale_alert_bot.py`

## 📊 Örnek Senaryolar

### Senaryo 1: High Alert Geldi
```
🚨 BTCUSDT - LONG (High) - $3M
→ Hemen TradingView'da BTC grafiğini aç
→ RSI, MACD kontrol et
→ Onay varsa LONG pozisyon aç
```

### Senaryo 2: 3x Medium SHORT
```
🚨 ETHUSDT - SHORT (Medium) x3
→ Trend dönüşü olabilir
→ SHORT pozisyon için hazırlan
→ Stop-loss koy
```

### Senaryo 3: Watchlist Alert
```
🚨 SOLUSDT (Watchlist) - LONG (Medium)
→ Portföyünüzdeki coin hareketlendi
→ Kar al veya pozisyon ekle kararı
```

## 🎓 Sonuç

Bu bot, **manuel takip yapmadan** whale hareketlerini **gerçek zamanlı** takip etmenizi sağlar. 

Alert geldiğinde:
1. ✅ Sesi duyun
2. ✅ Konsolu okuyun
3. ✅ Coin'i analiz edin
4. ✅ Bilinçli işlem açın

**Başarılar! 🚀**
