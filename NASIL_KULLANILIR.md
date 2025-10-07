# 🐋 WHALE ALERT BOT - HIZLI BAŞLANGIÇ

## 🚀 Nasıl Başlatılır

**Masaüstündeki kısayolu çift tıklayın:**
- 🖱️ "🐋 Whale Alert Bot" kısayoluna çift tıklayın
- ⏳ 10-15 saniye bekleyin
- ✅ Chrome penceresi açılacak (KAPATMAYIN!)
- 🔊 İlk alertler gelmeye başlayacak

## 📊 Ne Bekleyebilirsiniz

### İlk Başlangıç (10-15 saniye)
- Chrome açılır
- WhaleHunter'a login olur
- İlk 100 sinyal taranır
- **5-10 MEDIUM alert gelir** (ses + ekran)

### Çalışma Durumu
- Her 2 saniyede bir WhaleHunter'ı kontrol eder
- **YENİ** HIGH/MEDIUM sinyal gelince:
  - 🔊 Ses çalar (HIGH: 8 bip, MEDIUM: 2 bip)
  - 📢 Ekrana yazar
  - 💰 Coin, fiyat, hacim gösterir

### Yoğunluk Tespiti
- Bir coinde 30 dakikada 5+ sinyal → **ÖZEL UYARI!**
- 10 hızlı bip + büyük hareket mesajı
- Hangi yön dominant gösterir (LONG/SHORT)

## 🎯 Sinyal Filtreleri

✅ **HIGH Sinyaller**
- Her HIGH → Anında alert
- 8 bip (5 uzun + 3 hızlı yüksek perde)
- Kırmızı/sarı renkli ekran
- "HEMEN İŞLEM AÇMAYI DÜŞÜNÜN!" mesajı

✅ **MEDIUM Sinyaller**
- Her MEDIUM → Anında alert
- 2 bip
- Beyaz metin
- "Bu coini kontrol edin" mesajı

❌ **LOW Sinyaller**
- Tamamen görmezden geliniyor
- Spam önleme için

## 🛑 Nasıl Durdurulur

**3 Yöntem:**
1. Bot penceresinde **Ctrl+C** tuşlarına basın
2. Bot penceresini **X** ile kapatın
3. Task Manager → python.exe → End Task

## ⚠️ Önemli Notlar

### Chrome Penceresi
- **ASLA KAPATMAYIN!** Chrome kapanırsa bot durur
- Minimize edebilirsiniz (küçültün)
- Arka planda çalışmasına izin verin

### Sesler
- Bilgisayar sesinin açık olduğundan emin olun
- Her sinyal için bip gelir:
  - HIGH: 8 bip (dikkat çekici)
  - MEDIUM: 2 bip (orta)
  - Yoğunluk: 10 hızlı bip (acil)

### İlk Alertler
- İlk 10-15 saniyede 5-10 alert gelebilir
- Bu NORMALDIR! (Mevcut sinyalleri yüklüyor)
- Sonra sadece YENİ sinyaller için alert gelir

## 📈 Hangi Coinler Takip Ediliyor

**Watchlist (31 coin):**
- BTC, ETH, BNB, SOL, ADA, DOT, LINK, UNI, AVAX, MATIC
- AAVE, CAKE, CELO, DASH, DUSK, KAS, LDO, MANA, MAVIA
- NKN, ODER, OP, SAND, SKATE, ARPA, ASTER, AVNT, AXS
- VRTX, XLM, XRP, ZEC

**+ TÜM DİĞER COİNLER**
- WhaleHunter'da gelen tüm HIGH/MEDIUM sinyaller
- Watchlist'te olmasa bile alert gelir

## 🔧 Sorun Giderme

### "Bot başlamıyor"
- `.env` dosyasını kontrol edin
- WhaleHunter şifreniz doğru mu?
- İnternet bağlantınız var mı?

### "Ses gelmiyor"
- Bilgisayar sesini kontrol edin
- Volume mixer'da Python sesini açın
- Test: `scripts\test_live_alert.py` çalıştırın

### "Çok fazla alert geliyor"
- İlk 10-15 saniye normaldir
- Sonra sadece YENİ sinyaller gelir
- LOW sinyaller zaten kapalı

### "Chrome kapandı"
- Botu yeniden başlatın
- Chrome'un güncel olduğundan emin olun

## 📁 Dosya Yapısı

```
Kripto-Analiz/
├── START_WHALE_BOT.bat          ← Bu dosyayı çalıştırın
├── scripts/
│   ├── whale_alert_bot.py       ← Ana bot kodu
│   └── test_live_alert.py       ← Alert test scripti
├── .env                          ← WhaleHunter şifreleri
└── logs/                         ← Günlük loglar
```

## 💡 İpuçları

1. **7/24 Çalıştırın**: Bot elektrik kesintisi olmadıkça sürekli çalışabilir
2. **Minimize Edin**: Chrome penceresini küçültün, görmezden gelin
3. **Ses Açık**: Mutlaka ses açık olsun, yoksa alertleri kaçırırsınız
4. **İlk Dakika**: İlk 1 dakika alert gelebilir, sabırlı olun
5. **Coinleri Takip Edin**: Alert geldiğinde hemen Binance'de kontrol edin

## 🎓 Alert Örnekleri

### MEDIUM Alert
```
======================================================================
🚨 WHALE ALERT! 🚨
======================================================================
⏰ Zaman: 2025-10-06 01:45:23
📍 Coin: BTCUSDT
📊 Sinyal: Long (Medium)
💵 Fiyat: 62,450.00
📈 24h Değişim: +2.5%
💰 Hacim: 1,234,567 USDT
🎯 Sebep: 📊 MEDIUM Long SİNYALİ!
======================================================================
💡 İŞLEM ÖNERİSİ: Bu coini kontrol edin ve işlem açmayı düşünün!
======================================================================
```

### HIGH Alert
```
████████████████████████████████████████████████████████████████
🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥
║ ⚡⚡⚡ HIGH STRENGTH WHALE ALERT! ⚡⚡⚡
║ 
║ 📍 Coin: ETHUSDT
║ 💰 Hacim: 5,678,910 USDT
║ 
║ 🚀 HEMEN İŞLEM AÇMAYI DÜŞÜNÜN! 🚀
████████████████████████████████████████████████████████████████
```

---

**🎯 Hazırsınız! Masaüstündeki kısayola çift tıklayın ve alertleri beklemeye başlayın!** 🚀
