"""
Watchlist Verilerini Yavaşça Çek
Rate limit sorununu önlemek için her coin arasında bekleme ekler
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.tradingview.tv_client import TradingViewClient
from src.utils.data_manager import DataManager
from src.config.my_watchlist import MY_WATCHLIST

load_dotenv()


async def fetch_watchlist_slow():
    """Watchlist'i yavaşça çek (rate limit önleme)"""
    
    print("=" * 80)
    print("📊 KİŞİSEL WATCHLIST VERİ ÇEKME")
    print("=" * 80)
    print()
    
    print(f"📋 İzleme Listenizdeki Coinler: {len(MY_WATCHLIST)} adet\n")
    
    # Client oluştur
    tv_client = TradingViewClient()
    data_manager = DataManager()
    
    print("⏳ Veriler çekiliyor...")
    print("💡 Her coin arasında 3 saniye bekleniyor (rate limit için)\n")
    print("-" * 80)
    
    successful = []
    failed = []
    
    for i, symbol in enumerate(MY_WATCHLIST, 1):
        print(f"[{i:2}/{len(MY_WATCHLIST)}] {symbol:8} çekiliyor...", end=" ", flush=True)
        
        try:
            coin_data = await tv_client.fetch_coin_data(symbol)
            
            if coin_data:
                print(f"✅ ${coin_data['price']:>12,.4f} | RSI: {coin_data['rsi']:5.1f}")
                successful.append(coin_data)
            else:
                print(f"❌ Veri bulunamadı")
                failed.append(symbol)
            
            # Rate limit için bekle (son coin hariç)
            if i < len(MY_WATCHLIST):
                await asyncio.sleep(3)
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg:
                print(f"⏸️  Rate limit - Beklemede...")
                failed.append(symbol)
                # Rate limit durumunda daha uzun bekle
                await asyncio.sleep(10)
            else:
                print(f"❌ Hata: {error_msg[:50]}")
                failed.append(symbol)
    
    print("-" * 80)
    print()
    
    # Sonuç özeti
    print("=" * 80)
    print("📊 SONUÇ ÖZETİ")
    print("=" * 80)
    print()
    print(f"✅ Başarılı:  {len(successful):2}/{len(MY_WATCHLIST)} coin")
    print(f"❌ Başarısız: {len(failed):2}/{len(MY_WATCHLIST)} coin")
    print()
    
    if failed:
        print("⚠️  Çekilemeyen Coinler:")
        for symbol in failed:
            print(f"   • {symbol}")
        print()
    
    if successful:
        # Verileri kaydet
        print("💾 Veriler kaydediliyor...")
        data_manager.save_coins(successful, filename="watchlist_latest.json")
        data_manager.export_to_csv(successful, filename="watchlist_latest.csv")
        
        print("✅ Veriler data/ klasörüne kaydedildi!")
        print()
        
        # Hızlı özet
        print("📈 İlk 10 Coin:")
        print("-" * 80)
        for coin in successful[:10]:
            change = coin['change_24h']
            change_icon = "📈" if change > 0 else "📉"
            print(f"{coin['symbol']:8} | ${coin['price']:12,.4f} | "
                  f"{change_icon} {change:+6.2f}% | RSI: {coin['rsi']:5.1f}")
        
        if len(successful) > 10:
            print(f"... ve {len(successful) - 10} coin daha")
        
        print()
        print("💡 Detaylı analiz için:")
        print("   python scripts\\analyze_saved.py")
        print()
    
    else:
        print("❌ Hiç veri çekilemedi!")
        print()
        print("💡 Rate limit devam ediyor. Şunları deneyebilirsiniz:")
        print("   1. 15-30 dakika bekleyip tekrar deneyin")
        print("   2. Mevcut verileri kullanın: python scripts\\analyze_saved.py")
        print()
    
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(fetch_watchlist_slow())
