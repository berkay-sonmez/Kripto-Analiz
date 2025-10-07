"""
Canlı Alert Test Scripti
Gerçek alert görünümünü ve sesini test eder
"""
import winsound
import time
from datetime import datetime

def test_medium_alert():
    """MEDIUM sinyal alert testi"""
    print("\n" + "="*70)
    print("🧪 MEDIUM ALERT TEST BAŞLIYOR...")
    print("="*70 + "\n")
    
    time.sleep(1)
    
    # MEDIUM ses (2 bip)
    print("🔊 Ses çalıyor: 2 bip...")
    for _ in range(2):
        winsound.Beep(800, 200)
        time.sleep(0.1)
    
    # MEDIUM alert mesajı
    alert_message = f"""
{'='*70}
🚨 WHALE ALERT! 🚨
{'='*70}
⏰ Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Coin: BTCUSDT (TEST)
📊 Sinyal: Long (Medium)
💵 Fiyat: 62,450.00
📈 24h Değişim: +2.5%
💰 Hacim: 1,234,567 USDT
🎯 Sebep: 📊 MEDIUM Long SİNYALİ!
{'='*70}
💡 İŞLEM ÖNERİSİ: Bu coini kontrol edin ve işlem açmayı düşünün!
{'='*70}
    """
    print(alert_message)
    print("\n✅ MEDIUM alert testi tamamlandı!\n")

def test_high_alert():
    """HIGH sinyal alert testi"""
    print("\n" + "="*70)
    print("🧪 HIGH ALERT TEST BAŞLIYOR...")
    print("="*70 + "\n")
    
    time.sleep(1)
    
    # HIGH ses (8 bip - 5 uzun + 3 hızlı)
    print("🔊 Ses çalıyor: 8 bip (5 uzun + 3 hızlı yüksek perdeden)...")
    for i in range(5):
        winsound.Beep(1500, 300)
        time.sleep(0.15)
    for _ in range(3):
        winsound.Beep(2000, 150)
        time.sleep(0.05)
    
    # HIGH alert mesajı (KIRMIZI/SARI)
    alert_message = f"""
\033[91m{'█'*80}\033[0m
\033[93m{'█'*80}\033[0m
\033[91m{'█'*80}\033[0m
\033[93m╔{'═'*78}╗\033[0m
\033[93m║\033[91m{'🔥'*39}\033[93m║\033[0m
\033[93m║\033[91m           ⚡⚡⚡ HIGH STRENGTH WHALE ALERT! ⚡⚡⚡              \033[93m║\033[0m
\033[93m║\033[91m{'🔥'*39}\033[93m║\033[0m
\033[93m╠{'═'*78}╣\033[0m
\033[93m║\033[0m ⏰ Zaman: \033[96m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m
\033[93m║\033[0m 📍 Coin: \033[92mETHUSDT (TEST)\033[0m
\033[93m║\033[0m 📊 Sinyal: \033[91mLong (High)\033[0m
\033[93m║\033[0m 💵 Fiyat: 2,450.00
\033[93m║\033[0m 📈 24h Değişim: +5.8%
\033[93m║\033[0m 💰 Hacim: \033[95m5,678,910 USDT\033[0m
\033[93m║\033[0m 🎯 Sebep: \033[91m⚡ HIGH STRENGTH SİNYAL!\033[0m
\033[93m╠{'═'*78}╣\033[0m
\033[93m║\033[91m  🚀 HEMEN İŞLEM AÇMAYI DÜŞÜNÜN! BÜYÜK HAMLENİN TAM ZAMANI! 🚀  \033[93m║\033[0m
\033[93m╚{'═'*78}╝\033[0m
\033[91m{'█'*80}\033[0m
\033[93m{'█'*80}\033[0m
\033[91m{'█'*80}\033[0m
    """
    print(alert_message)
    print("\n✅ HIGH alert testi tamamlandı!\n")

def test_high_activity():
    """Yoğun aktivite alert testi"""
    print("\n" + "="*70)
    print("🧪 YOĞUN AKTİVİTE ALERT TEST BAŞLIYOR...")
    print("="*70 + "\n")
    
    time.sleep(1)
    
    # Yoğunluk sesi (10 hızlı bip)
    print("🔊 Ses çalıyor: 10 hızlı bip...")
    for _ in range(10):
        winsound.Beep(1800, 100)
        time.sleep(0.05)
    
    # Yoğunluk alert mesajı
    alert_message = f"""
{'🔥'*80}
{'⚠️ '*40}
║ 
║ 🚨🚨🚨 YOĞUN AKTİVİTE TESPİT EDİLDİ! 🚨🚨🚨
║ 
║ 💎 Coin: SOLUSDT (TEST)
║ 📊 Sinyal Sayısı: 7 sinyal / 30 dakika
║ 📈 Yön: 5 LONG / 2 SHORT → LONG dominant
║ 
║ 💡 Analiz: Bu coin ÇOK HAREKETLÜ! Büyük bir hareket başlıyor olabilir.
║          30 dakikada 7 whale sinyali geldi!
║ 
║ 🎯 Öneri: Bu coini ŞİMDİ detaylı analiz et ve pozisyon açmayı düşün!
║          Trend LONG yönünde güçlü görünüyor.
║ 
{'⚠️ '*40}
{'🔥'*80}
    """
    print(alert_message)
    print("\n✅ Yoğun aktivite alert testi tamamlandı!\n")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎯 WHALE ALERT SİSTEMİ - CANLI TEST")
    print("="*70)
    print("\n📋 Bu test 3 farklı alert tipini gösterecek:")
    print("   1. MEDIUM sinyal (2 bip)")
    print("   2. HIGH sinyal (8 bip - KIRMIZI/SARI)")
    print("   3. Yoğun aktivite (10 bip)")
    print("\n⚠️  Not: Ses geldiğinde hoparlör sesini kontrol edin!")
    print("="*70)
    
    input("\n▶️  ENTER'a basın ve testi başlatın...")
    
    # 1. MEDIUM test
    test_medium_alert()
    time.sleep(2)
    
    # 2. HIGH test
    test_high_alert()
    time.sleep(2)
    
    # 3. Yoğunluk test
    test_high_activity()
    
    print("\n" + "="*70)
    print("✅ TÜM TESTLER TAMAMLANDI!")
    print("="*70)
    print("\n💡 Bot çalışırken bu şekilde alertler gelecek!")
    print("   • MEDIUM → 2 bip, beyaz metin")
    print("   • HIGH → 8 bip, kırmızı/sarı metin")
    print("   • Yoğunluk → 10 bip, özel uyarı")
    print("\n🚀 Bot şu anda çalışıyor ve gerçek sinyalleri bekliyor!\n")
