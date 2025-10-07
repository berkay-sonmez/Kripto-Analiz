"""
WhaleHunter Anlık Sinyal Analizi
HIGH sinyaller ve büyük hacimli LONG/SHORT hareketlerini gösterir
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.selenium_whalehunter import WhaleHunterSeleniumScraper
import json
from datetime import datetime

print("=" * 80)
print("🐋 WHALEHUNTER ANLıK SİNYAL ANALİZİ")
print("=" * 80)
print(f"Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# .env dosyasından credentials
from dotenv import load_dotenv
load_dotenv()

email = os.getenv("WHALEHUNTER_EMAIL")
password = os.getenv("WHALEHUNTER_PASSWORD")

# Scraper başlat
scraper = WhaleHunterSeleniumScraper(email, password)
scraper.setup_driver()
scraper.login()
scraper.go_to_futures_page()

import time
time.sleep(5)

# Verileri çek (60 saniye bekle)
signals = scraper.wait_for_data(duration_seconds=60)
scraper.close()

# Filtreleme
vet_signals = [s for s in signals if 'VET' in s['symbol'].upper()]
high_signals = [s for s in signals if 'High' in s.get('strength', '')]

# Büyük hacimli sinyaller (1M+ USDT)
big_volume = []
for s in signals:
    try:
        volume = float(s['total_usdt'].replace(',', ''))
        if volume >= 1000000:  # 1M+
            big_volume.append((s, volume))
    except:
        pass

big_volume.sort(key=lambda x: x[1], reverse=True)

# VET Sinyalleri
print("\n" + "=" * 80)
print("📊 VET SİNYALLERİ")
print("=" * 80)
if vet_signals:
    for s in vet_signals[:10]:
        print(f"🪙 {s['symbol']:15} | {s['signal_type']:5} | {s['strength']:6} | Hacim: {s['total_usdt']:>15} | Fiyat: {s['last_price']}")
else:
    print("❌ VET sinyali bulunamadı!")

# HIGH Sinyaller
print("\n" + "=" * 80)
print("⚡ HIGH STRENGTH SİNYALLER")
print("=" * 80)
if high_signals:
    for s in high_signals[:15]:
        emoji = "📈" if s['signal_type'] == 'Long' else "📉"
        print(f"{emoji} {s['symbol']:15} | {s['signal_type']:5} | {s['strength']:6} | Hacim: {s['total_usdt']:>15} | Değişim: {s['change_24h']}")
else:
    print("❌ HIGH sinyal bulunamadı!")

# Büyük Hacimli İşlemler (1M+)
print("\n" + "=" * 80)
print("💰 BÜYÜK HACİMLİ İŞLEMLER (1M+ USDT)")
print("=" * 80)
if big_volume:
    for s, vol in big_volume[:20]:
        emoji = "🟢" if s['signal_type'] == 'Long' else "🔴"
        print(f"{emoji} {s['symbol']:15} | {s['signal_type']:5} | {s['strength']:6} | Hacim: ${vol:>12,.0f} | Fiyat: {s['last_price']:>10} | Değişim: {s['change_24h']}")
else:
    print("❌ 1M+ hacimli sinyal bulunamadı!")

# İstatistikler
print("\n" + "=" * 80)
print("📈 İSTATİSTİKLER")
print("=" * 80)
print(f"Toplam Sinyal: {len(signals)}")
print(f"HIGH Sinyal: {len(high_signals)}")
print(f"VET Sinyal: {len(vet_signals)}")
print(f"1M+ Hacim: {len(big_volume)}")

# Strength dağılımı
high_count = len([s for s in signals if 'High' in s.get('strength', '')])
medium_count = len([s for s in signals if 'Medium' in s.get('strength', '')])
low_count = len([s for s in signals if 'Low' in s.get('strength', '')])

print(f"\nStrength Dağılımı:")
print(f"  HIGH: {high_count}")
print(f"  MEDIUM: {medium_count}")
print(f"  LOW: {low_count}")

# LONG/SHORT dağılımı
long_count = len([s for s in signals if s.get('signal_type') == 'Long'])
short_count = len([s for s in signals if s.get('signal_type') == 'Short'])

print(f"\nLONG/SHORT Dağılımı:")
print(f"  LONG: {long_count}")
print(f"  SHORT: {short_count}")

print("\n" + "=" * 80)
print("✅ Analiz tamamlandı!")
print("=" * 80)
