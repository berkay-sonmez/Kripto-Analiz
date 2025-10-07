# 🎯 HIZLI BAŞLANGIÇ - Whale Bot Kalıcı Çalışma

## 📌 Şu Anda Durum

❌ **Terminal'den çalışıyor** → Terminal kapanınca bot da kapanır  
✅ **Alertler geliyor** → Sistem doğru çalışıyor

---

## 🚀 3 Basit Adım - Kalıcı Hale Getirme

### 1️⃣ Şu Anki Bot'u Durdur

Terminal'e git ve `Ctrl + C` bas

### 2️⃣ Yeni Başlatma Yöntemi

**ÇİFT TIKLA:**
```
start_whale_bot.bat
```

Bu:
- ✅ Bot'u **minimize pencerede** başlatır
- ✅ Terminal kapanabilir, bot **çalışmaya devam eder**
- ✅ Alert geldiğinde **bip sesi** duyarsınız

### 3️⃣ Kontrol Et

1. `Ctrl + Shift + Esc` → Task Manager aç
2. **Details** sekmesi → `python.exe` görünmeli
3. CPU: %1-5 arası normal

---

## 🔄 Bot Çalışıyor mu Nasıl Anlarım?

✅ **Task Manager'da** `python.exe` var  
✅ **Alert geldiğinde** bip sesi duyuyorsun  
✅ **CPU kullanımı** sabit (%1-5)

---

## 🛑 Durdurmak İçin

**Task Manager:**
1. `Ctrl + Shift + Esc`
2. Details → `python.exe` bul
3. Sağ tık → **End Task**

**Veya PowerShell:**
```powershell
Get-Process python | Stop-Process -Force
```

---

## 🌟 İlerisi İçin - Bilgisayar Açılınca Otomatik

### Adım 1: Başlangıç Klasörü
```
Win + R → shell:startup → Enter
```

### Adım 2: Kısayol Kopyala
1. `start_whale_bot.bat` dosyasına **sağ tık**
2. **Copy**
3. `shell:startup` klasörüne **Paste Shortcut**

### Sonuç
✅ Bilgisayar açıldığında bot **otomatik başlar**  
✅ Giriş yaptıktan 30 saniye sonra **hazır**

---

## 📊 Alert Ayarları

### Çok Fazla Alert Geliyorsa

`.env` dosyasını aç:
```powershell
notepad .env
```

Değiştir:
```env
MIN_VOLUME=50000  # $50k (şu an $10k)
```

### Az Alert Geliyorsa

```env
MIN_VOLUME=5000   # $5k
```

**Bot'u yeniden başlat** değişiklik için!

---

## 🎊 ÖZETİ ÖZET

1. **Şimdi**: Çift tıkla `start_whale_bot.bat`
2. **İleride**: Başlangıç klasörüne kısayol at
3. **Detaylar**: `docs\KALICI_ARKAPLAN_KILAVUZU.md` oku

**BU KADAR! 🚀**
