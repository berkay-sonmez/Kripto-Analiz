# 🚀 Whale Bot - Kalıcı Arka Plan Çalışma Kılavuzu

## 🎯 Problem

**Terminal kapatıldığında bot da kapanır.** Bilgisayarı kapatana kadar sürekli çalışması için özel kurulum gerekiyor.

---

## ✅ Çözüm 1: Hızlı Başlatma (BAT/PS1 Script)

### Kullanım

1. **Çift tıkla**: `start_whale_bot.bat`
2. Bot **minimize pencerede** başlar
3. **Terminal kapatılabilir** ama bot çalışmaya devam eder

### Durdurmak İçin

1. `Ctrl + Shift + Esc` → Task Manager aç
2. **Details** sekmesine git
3. `python.exe` bul ve **End Task**

---

## ✅ Çözüm 2: Windows Başlangıçta Otomatik Çalıştırma

### Adım 1: Başlangıç Klasörünü Aç

```
Win + R → shell:startup → Enter
```

### Adım 2: Kısayol Oluştur

1. `start_whale_bot.bat` dosyasına **sağ tık**
2. **Copy** seç
3. `shell:startup` klasörüne **Paste Shortcut**

### Sonuç

✅ **Bilgisayar açıldığında** bot otomatik başlar  
✅ **Giriş yaptıktan sonra** arka planda çalışır  
✅ **Siz hiçbir şey yapmadan** whale takibi devam eder

---

## ✅ Çözüm 3: Task Scheduler (En Profesyonel)

### Adım 1: Task Scheduler'ı Aç

```
Win + R → taskschd.msc → Enter
```

### Adım 2: Yeni Task Oluştur

1. Sağ panel: **Create Basic Task**
2. Name: `Whale Alert Bot`
3. Description: `Kripto whale hareketleri takibi`

### Adım 3: Trigger (Tetikleyici)

- **When I log on** seç → Next

### Adım 4: Action (Eylem)

- **Start a program** seç → Next

**Program/script:**
```
C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz\.venv\Scripts\python.exe
```

**Add arguments:**
```
scripts\whale_alert_bot.py
```

**Start in:**
```
C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz
```

### Adım 5: Gelişmiş Ayarlar

Task'a sağ tık → **Properties**

**General sekmesi:**
- ✅ Run whether user is logged on or not
- ✅ Run with highest privileges
- ✅ Hidden (gizli çalışır, pencere görmezsiniz)

**Conditions sekmesi:**
- ❌ Stop if the computer switches to battery power (kapatın - laptop için)
- ❌ Start the task only if the computer is on AC power (kapatın)

**Settings sekmesi:**
- ✅ Allow task to be run on demand
- ✅ Run task as soon as possible after a scheduled start is missed
- ❌ Stop the task if it runs longer than (kapatın - sürekli çalışsın)
- ✅ If the running task does not end when requested, force it to stop
- **If the task fails, restart every:** `5 minutes` (3 attempt)

### Sonuç

✅ **Bilgisayar açıldığında** otomatik başlar  
✅ **Kapansa bile** 5 dakika sonra tekrar başlar  
✅ **Gizli mod** - hiçbir pencere görmezsiniz  
✅ **Windows servisi gibi** çalışır

---

## 📊 Test Etme

### Bot Çalışıyor mu Kontrol

1. `Ctrl + Shift + Esc` → Task Manager
2. **Details** sekmesi
3. `python.exe` var mı bak
4. CPU kullanımı: %1-5 arası normal

### Alert Geliyor mu Test

WhaleHunter'da büyük hacimli işlem olduğunda:
- 🔊 **Bip sesi** duymalısınız
- 💬 **Console log** (eğer terminal açıksa)

---

## 🛑 Bot'u Durdurmak

### Yöntem 1: Task Manager
```
Ctrl + Shift + Esc → Details → python.exe → End Task
```

### Yöntem 2: PowerShell
```powershell
# Tüm Python processleri durdur
Get-Process python | Stop-Process -Force
```

### Yöntem 3: Task Scheduler'dan
```
Win + R → taskschd.msc → Whale Alert Bot → sağ tık → End
```

---

## 🔄 Yeniden Başlatma

### Manuel
- Çift tıkla: `start_whale_bot.bat`

### Otomatik (Scheduled Task varsa)
- Bilgisayarı yeniden başlat
- 30 saniye içinde bot otomatik başlar

---

## 🐛 Sorun Giderme

### "Bot çalışmıyor, alert gelmiyor"

**Kontrol:**
```powershell
# Terminal aç
cd C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz
.\.venv\Scripts\python.exe scripts\whale_alert_bot.py
```

**Log kontrol:**
- `logs/` klasörüne bak
- Son log dosyasını aç
- Hata var mı?

### "ChromeDriver hatası"

```powershell
# ChromeDriver güncelle
.\.venv\Scripts\pip.exe install --upgrade webdriver-manager
```

### "Login olmuyor"

`.env` dosyasını kontrol et:
```powershell
notepad .env
```

```env
WHALEHUNTER_EMAIL=berkaysnmz1903@gmail.com
WHALEHUNTER_PASSWORD=1327pc1327
MIN_VOLUME=10000
```

### "Çok fazla/az alert geliyor"

`.env` dosyasında `MIN_VOLUME` değiştir:

```env
# Çok fazla alert → Hacmi artır
MIN_VOLUME=50000

# Az alert → Hacmi azalt
MIN_VOLUME=5000
```

Sonra bot'u **yeniden başlat**.

---

## 📈 Önerilen Kurulum

### İlk Kurulum (Test)
1. Manuel başlat: `start_whale_bot.bat`
2. 1-2 saat izle
3. Alert sayısını kontrol et
4. MIN_VOLUME ayarla

### Stabil Olduktan Sonra
1. Task Scheduler kurulumu yap
2. Bilgisayarı yeniden başlat
3. Task Manager'dan kontrol et
4. Artık **rahat bırakabilirsiniz**

---

## 💡 Pro İpuçları

### Gece Sessiz Mod

`whale_alert_bot.py` içinde `play_alert_sound()` fonksiyonunu düzenle:

```python
def play_alert_sound(self, strength: str):
    from datetime import datetime
    hour = datetime.now().hour
    
    # Gece 23:00 - 07:00 arası sessiz
    if hour >= 23 or hour <= 7:
        return
    
    # Normal ses
    if strength == 'High':
        for _ in range(3):
            winsound.Beep(1000, 200)
            import time
            time.sleep(0.1)
    # ... rest of code
```

### Telegram Bildirimi (Gelecek)

Mobil cihazda da alert almak için Telegram bot entegrasyonu eklenebilir.

### Log Rotation

Loglar çok büyürse `loguru` otomatik temizler ama manuel temizlik:

```powershell
# 7 günden eski logları sil
Get-ChildItem logs\*.log | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item
```

---

## ✅ Sonuç

**Bu 3 yöntemden birini kullanarak** bot'u kalıcı hale getirebilirsiniz:

1. **BAT Script** → Hızlı test için
2. **Startup Folder** → Basit otomatik başlangıç
3. **Task Scheduler** → Profesyonel, en güvenilir

**Task Scheduler** en iyi seçenek - bot kapansa bile otomatik yeniden başlar!

---

## 🚀 Şimdi Ne Yapmalısınız?

1. **Terminali kapat** (şu anki bot durur)
2. **Çift tıkla**: `start_whale_bot.bat`
3. **Bot minimize başlar**, terminal kapanır ama **bot çalışır**
4. **Task Manager'dan** kontrol et
5. **1 saat bekle** ve alert sayısına bak
6. **Memnun kalırsan** Task Scheduler kur

**Başarılar! 🎉**
