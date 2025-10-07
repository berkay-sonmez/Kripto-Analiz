# 🚀 Whale Alert Bot - 24/7 Arka Plan Çalışma Kılavuzu

## 🎯 Amaç

Bu bot **bilgisayarınızda sürekli arka planda** çalışarak whale (balina) hareketlerini takip eder ve **sadece gerçekten önemli** sinyallerde sizi uyarır.

## 🛡️ Güçlendirilmiş Filtreler

### 1️⃣ Minimum Hacim Filtresi
- **Varsayılan**: $50,000 USDT
- **Amaç**: Küçük, önemsiz hareketleri filtreler
- **Değiştirme**: `.env` dosyasında `MIN_VOLUME=100000` (örn: $100k)

### 2️⃣ Cooldown Sistemi
- **Süre**: 30 dakika
- **Amaç**: Aynı coin için spam alert önleme
- **Mantık**: Bir coinden alert aldıktan sonra 30 dakika o coin sessiz

### 3️⃣ Pattern Şartları

| Durum | Şart | Alert |
|-------|------|-------|
| **HIGH sinyal** | Büyük hacim + cooldown geçmiş | ✅ Anında |
| **MEDIUM (normal coin)** | 3 kez üst üste + hacim + cooldown | ✅ Alert |
| **MEDIUM (watchlist)** | 2 kez üst üste + hacim + cooldown | ✅ Alert |
| **LOW sinyal** | - | ❌ Alert YOK |

## 🕐 24/7 Sürekli Çalışma

### Windows'da Arka Planda Başlatma

#### Yöntem 1: PowerShell ile Minimize
```powershell
# 1. Bot'u başlat
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz'; .\.venv\Scripts\python.exe scripts\whale_alert_bot.py" -WindowStyle Minimized
```

#### Yöntem 2: Başlangıçta Otomatik Çalıştırma

1. **Başlat klasörüne kısayol ekle:**
   ```
   Win + R → shell:startup
   ```

2. **Batch dosyası oluştur** (`whale_bot_start.bat`):
   ```batch
   @echo off
   cd /d "C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz"
   start /min "" ".venv\Scripts\python.exe" "scripts\whale_alert_bot.py"
   ```

3. Bu `.bat` dosyasını `shell:startup` klasörüne kopyala

#### Yöntem 3: Task Scheduler (En Profesyonel)

1. **Task Scheduler'ı aç**: `Win + R → taskschd.msc`

2. **Create Basic Task**:
   - Name: `Whale Alert Bot`
   - Trigger: `When I log on`
   - Action: `Start a program`
   - Program: `C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz\.venv\Scripts\python.exe`
   - Arguments: `scripts\whale_alert_bot.py`
   - Start in: `C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz`

3. **Properties (Gelişmiş Ayarlar)**:
   - ✅ Run whether user is logged on or not
   - ✅ Hidden (arka planda gizli çalışır)
   - ✅ If task fails, restart every 5 minutes

## 📊 İzleme Stratejisi

### Tüm Gün Açık (Önerilen)
```powershell
# Bot sürekli çalışır, siz başka işlerle ilgilenirsiniz
python scripts\whale_alert_bot.py
```

**Avantajları:**
- ✅ Hiçbir whale hareketini kaçırmazsınız
- ✅ 30 dakika cooldown sayesinde spam yok
- ✅ Sadece önemli sinyaller gelir

### Önemli Saatler

#### Yüksek Volatilite Saatleri
1. **08:00-10:00** (Türkiye): Avrupa açılışı
2. **14:00-16:00** (Türkiye): Avrupa kapanış + Amerika açılış
3. **20:00-22:00** (Türkiye): Amerika ana seansı
4. **01:00-03:00** (Türkiye): Asya seansı

**Tüm gün çalışsın ama siz bu saatlerde bilgisayarın yanında olun**

## 🎚️ Filtre Ayarları

### Daha Az Alert İstiyorsanız

`.env` dosyasında:
```env
MIN_VOLUME=100000  # $100k (varsayılan $50k)
```

`whale_alert_bot.py` içinde (satır ~32):
```python
self.cooldown_minutes = 60  # 60 dakika (varsayılan 30)
```

### Daha Fazla Alert İstiyorsanız

```env
MIN_VOLUME=20000  # $20k
```

```python
self.cooldown_minutes = 15  # 15 dakika
```

**Watchlist coinleri için** MEDIUM x2 yeterli (zaten daha hassas)

## 🔊 Ses Ayarları

### Sesi Tamamen Kapatmak
`play_alert_sound()` fonksiyonunu devre dışı bırak:

```python
def play_alert_sound(self, strength: str):
    return  # Ses kapalı
```

### Sesi Özelleştirmek
```python
# HIGH için daha uzun bip
winsound.Beep(1200, 500)  # 1200Hz, 500ms

# MEDIUM için kısa bip
winsound.Beep(800, 150)   # 800Hz, 150ms
```

## 📈 Alert Geldiğinde Ne Yapmalı?

### 1. Konsolu Kontrol Edin
```
🚨 WHALE ALERT! 🚨
📍 Coin: BTCUSDT
📊 Sinyal: LONG (High)
💰 Hacim: $5,123,456
🎯 Sebep: ⚡ HIGH STRENGTH SİNYAL!
```

### 2. TradingView'da Doğrulayın
```
1. TradingView'ı açın
2. BTCUSDT grafiğine gidin
3. RSI, MACD, Volume kontrol edin
4. Desteği/direnci görün
```

### 3. İşlem Kararı
- **HIGH sinyal** → Güçlü hareket, hızlı değerlendirin
- **MEDIUM x3** → Trend başlangıcı, pozisyon alabilirsiniz
- **Watchlist** → Portföyünüzdeki coin, dikkatli olun

### 4. Stop-Loss Koymayı Unutmayın
```
Long: %5-10 altına stop
Short: %5-10 üstüne stop
```

## 🔄 Yeniden Başlatma

### Bot Crashed (Kapandı)
```powershell
# Tekrar başlat
python scripts\whale_alert_bot.py
```

### Chrome Hatası
```powershell
# ChromeDriver güncelle
pip install --upgrade webdriver-manager
```

### Login Hatası
```powershell
# .env kontrol et
notepad .env

# Şifrenizi doğrulayın
```

## 📊 İstatistikler

### Günlük Beklenen Alert Sayısı

**Normal Piyasa** (Düşük volatilite):
- 5-10 alert/gün
- Çoğu MEDIUM x3 pattern

**Volatil Piyasa** (Yüksek hareket):
- 15-25 alert/gün
- HIGH sinyaller artar

**Çok Volatil** (Bitcoin %10+ hareket):
- 30-50 alert/gün
- Sürekli HIGH sinyaller

### 30 Dakika Cooldown Etkisi

Örnek: BTCUSDT'de HIGH sinyal geldi (19:00)
- ✅ 19:00: Alert verilir
- ❌ 19:15: Yeni sinyal ama cooldown aktif
- ❌ 19:25: Yine cooldown
- ✅ 19:30: Cooldown bitti, yeni sinyal olursa alert

**Sonuç**: Aynı coinden max 48 alert/gün (24 saat ÷ 0.5 saat)

## 🎯 Önerilen Kurulum

### Başlangıç İçin
```env
MIN_VOLUME=50000        # $50k
cooldown_minutes=30     # 30 dakika
duration_minutes=0      # Sürekli
```

### 1 Hafta Sonra Ayarlayın
Çok az alert geliyorsa:
```env
MIN_VOLUME=30000        # $30k'ya düşür
cooldown_minutes=20     # 20 dakika
```

Çok fazla alert geliyorsa:
```env
MIN_VOLUME=100000       # $100k'ya çıkar
cooldown_minutes=45     # 45 dakika
```

## 🌙 Gece Modunda Çalışma

### Sesi Kapatıp Sadece Log
```python
# play_alert_sound() içinde:
if datetime.now().hour >= 23 or datetime.now().hour <= 7:
    return  # Gece sessiz
```

### Sadece Kritik Sinyaller Gece
```python
# check_signal_pattern() başında:
if datetime.now().hour >= 23 or datetime.now().hour <= 7:
    if 'High' not in strength:
        return False  # Gece sadece HIGH
```

## 💪 Başarı İçin İpuçları

1. **İlk Gün**: Tüm alert'leri izleyin, sistemi öğrenin
2. **İkinci Gün**: Filtrelerinizi ayarlayın (hacim, cooldown)
3. **Üçüncü Gün**: Arka planda çalıştırın, sadece alert'lere odaklanın
4. **Bir Hafta**: Winning pattern'lerinizi not edin
5. **Sürekli**: Otomatik başlangıç ayarlayın, rahat edin

## 🚫 Yapmamanız Gerekenler

❌ Her alert'te işlem açmayın → %60-70'inde açın
❌ Stop-loss koymadan işlem açmayın
❌ Aynı anda çok fazla pozisyon açmayın (max 3-5)
❌ Alert'i görmezden gelmeyin (sonra pişman olursunuz)
❌ Filtrelerinizi çok gevşek tutmayın (spam olur)

## ✅ Yapmanız Gerekenler

✅ Bot'u 24/7 açık tutun (arka planda)
✅ Alert gelince TradingView'da doğrulayın
✅ Demo hesapta test edin (ilk hafta)
✅ İstatistiklerinizi tutun (kaç alert, kaç işlem, success rate)
✅ Filtrelerinizi ayarlayın (kendi stratejinize göre)

---

## 🎊 Sonuç

**Bu sistem ile whale'leri kaçırmadan, spam'e boğulmadan 24/7 piyasayı takip edebilirsiniz!**

- ✅ Sürekli çalışır
- ✅ Sadece önemli sinyaller
- ✅ Cooldown ile spam önleme
- ✅ Hacklenebilir filtreler
- ✅ Arka plan modu

**Başarılar! 🚀**
