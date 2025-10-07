"""
Watchlist Test - Küçük Grup
Rate limit problemini önlemek için az sayıda coin ile test
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.tradingview.tv_client import TradingViewClient

load_dotenv()


async def test_small_batch():
    """Küçük bir coin grubu ile test et"""
    
    print("🧪 Veri Çekme Testi\n")
    print("=" * 60)
    
    # Test için sadece 3 coin
    test_coins = ["BTC", "ETH", "SOL"]
    
    print(f"📊 Test Edilecek Coinler: {', '.join(test_coins)}\n")
    
    tv_client = TradingViewClient()
    
    print("⏳ Veriler çekiliyor (her coin arasında 2 saniye bekleme)...\n")
    
    results = []
    for i, symbol in enumerate(test_coins, 1):
        print(f"[{i}/{len(test_coins)}] {symbol} çekiliyor...", end=" ")
        
        try:
            coin_data = await tv_client.fetch_coin_data(symbol)
            
            if coin_data:
                print(f"✅ ${coin_data['price']:,.2f}")
                results.append(coin_data)
            else:
                print("❌ Başarısız")
            
            # Rate limit için bekle
            if i < len(test_coins):
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    print("\n" + "=" * 60)
    
    if results:
        print(f"\n✅ Başarı! {len(results)}/{len(test_coins)} coin çekildi\n")
        
        print("📊 Sonuçlar:")
        print("-" * 60)
        for coin in results:
            print(f"{coin['symbol']:8} | ${coin['price']:12,.2f} | RSI: {coin['rsi']:5.1f} | {coin['recommendation']}")
        
        print("\n✅ Sistem çalışıyor! Şimdi tüm watchlist'i deneyebilirsiniz.")
        print("   Komut: python scripts\\analyze_watchlist.py\n")
        
        return True
    else:
        print("\n❌ Hiç veri çekilemedi!")
        print("\n💡 Muhtemel sebepler:")
        print("  • TradingView API geçici olarak erişilemez")
        print("  • Rate limit (çok fazla istek)")
        print("  • İnternet bağlantısı sorunu")
        print("\n💡 Çözüm: 5-10 dakika bekleyip tekrar deneyin.\n")
        
        return False


if __name__ == "__main__":
    success = asyncio.run(test_small_batch())
