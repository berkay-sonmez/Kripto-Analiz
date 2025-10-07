"""
HIGH vs MEDIUM Alert Testi
Renk farklarını görmek için
"""

from datetime import datetime
import winsound
import time

def test_high_alert():
    """HIGH strength alert örneği"""
    symbol = "BTCUSDT"
    signal_type = "Long"
    strength = "High"
    price = "62,345.50"
    change_24h = "+5.67%"
    volume = "15,234,567"
    reason = "⚡ HIGH STRENGTH SİNYAL!"
    
    # 🔥 HIGH SİNYAL - KIRMIZI/SARI RENK!
    alert_message = f"""
\033[91m{'█'*80}\033[0m
\033[93m{'█'*80}\033[0m
\033[91m{'█'*80}\033[0m
\033[93m╔{'═'*78}╗\033[0m
\033[93m║\033[91m{'🔥'*39}\033[93m║\033[0m
\033[93m║\033[91m           ⚡⚡⚡ HIGH STRENGTH WHALE ALERT! ⚡⚡⚡              \033[93m║\033[0m
\033[93m║\033[91m{'🔥'*39}\033[93m║\033[0m
\033[93m╠{'═'*78}╣\033[0m
\033[93m║\033[0m ⏰ Zaman: \033[96m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m{' '*(80-len(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))-13)}\033[93m║\033[0m
\033[93m║\033[0m 📍 Coin: \033[92m{symbol}\033[0m{' '*(80-len(symbol)-13)}\033[93m║\033[0m
\033[93m║\033[0m 📊 Sinyal: \033[91m{signal_type} ({strength})\033[0m{' '*(80-len(signal_type)-len(strength)-15)}\033[93m║\033[0m
\033[93m║\033[0m 💵 Fiyat: {price}{' '*(80-len(str(price))-13)}\033[93m║\033[0m
\033[93m║\033[0m 📈 24h Değişim: {change_24h}{' '*(80-len(str(change_24h))-19)}\033[93m║\033[0m
\033[93m║\033[0m 💰 Hacim: \033[95m{volume} USDT\033[0m{' '*(80-len(str(volume))-18)}\033[93m║\033[0m
\033[93m║\033[0m 🎯 Sebep: \033[91m{reason}\033[0m{' '*(80-len(reason)-13)}\033[93m║\033[0m
\033[93m╠{'═'*78}╣\033[0m
\033[93m║\033[91m  🚀 HEMEN İŞLEM AÇMAYI DÜŞÜNÜN! BÜYÜK HAMLENİN TAM ZAMANI! 🚀  \033[93m║\033[0m
\033[93m╚{'═'*78}╝\033[0m
\033[91m{'█'*80}\033[0m
\033[93m{'█'*80}\033[0m
\033[91m{'█'*80}\033[0m
    """
    
    print(alert_message)
    
    # SES
    print("\n🔊 HIGH STRENGTH ALARM! (5x bip + 3x hızlı)")
    for i in range(5):
        winsound.Beep(1500, 300)
        time.sleep(0.15)
    for _ in range(3):
        winsound.Beep(2000, 150)
        time.sleep(0.05)

def test_medium_alert():
    """MEDIUM strength alert örneği"""
    symbol = "ETHUSDT"
    signal_type = "Short"
    strength = "Medium"
    price = "2,634.52"
    change_24h = "-2.34%"
    volume = "456,789"
    reason = "📊 MEDIUM Short SİNYALİ!"
    
    alert_message = f"""
{'='*70}
🚨 WHALE ALERT! 🚨
{'='*70}
⏰ Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Coin: {symbol}
📊 Sinyal: {signal_type} ({strength})
💵 Fiyat: {price}
📈 24h Değişim: {change_24h}
💰 Hacim: {volume} USDT
🎯 Sebep: {reason}
{'='*70}
💡 İŞLEM ÖNERİSİ: Bu coini kontrol edin ve işlem açmayı düşünün!
{'='*70}
    """
    
    print(alert_message)
    
    # SES
    print("🔊 Medium alert (2x bip)")
    for _ in range(2):
        winsound.Beep(800, 200)
        time.sleep(0.1)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔥 HIGH STRENGTH ALERT TEST")
    print("="*80)
    test_high_alert()
    
    time.sleep(2)
    
    print("\n\n" + "="*80)
    print("📊 MEDIUM STRENGTH ALERT TEST")
    print("="*80)
    test_medium_alert()
    
    print("\n\n✅ Test tamamlandı!")
    print("Fark gördünüz mü? HIGH alert KIRMIZI/SARI renkli ve daha uzun ses!")
