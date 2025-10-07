"""
Altcoin Verilerini Çekme Script
Hızlı test ve veri toplama için
"""

import asyncio
import sys
import os
from pathlib import Path

# Proje kök dizinini path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.tradingview.tv_client import TradingViewClient
from src.utils.data_manager import DataManager

load_dotenv()


async def main():
    """Altcoinleri çek ve kaydet"""
    print("🚀 Altcoin verileri çekiliyor...\n")
    
    # Client oluştur
    tv_client = TradingViewClient()
    data_manager = DataManager()
    
    # Verileri çek
    coins = await tv_client.fetch_all_altcoins()
    
    if not coins:
        print("❌ Veri çekilemedi!")
        return
    
    # Özet göster
    print(f"\n✅ Toplam {len(coins)} coin çekildi\n")
    print("📊 İlk 10 coin:")
    print("-" * 60)
    for coin in coins[:10]:
        symbol = coin['symbol']
        price = coin['price']
        change = coin['change_24h']
        rsi = coin['rsi']
        rec = coin['recommendation']
        
        change_icon = "📈" if change > 0 else "📉"
        print(f"{symbol:8} | ${price:12,.2f} | {change_icon} {change:+6.2f}% | RSI: {rsi:5.1f} | {rec}")
    
    # Kaydet
    data_manager.save_coins(coins)
    data_manager.export_to_csv(coins)
    
    # Top movers
    movers = tv_client.get_top_movers(coins, limit=5)
    
    print("\n🔥 En Çok Yükselenler:")
    for coin in movers['top_gainers']:
        print(f"  • {coin['symbol']}: +{coin['change_24h']:.2f}%")
    
    print("\n❄️  En Çok Düşenler:")
    for coin in movers['top_losers']:
        print(f"  • {coin['symbol']}: {coin['change_24h']:.2f}%")
    
    print("\n✅ Veriler data/ klasörüne kaydedildi!")


if __name__ == "__main__":
    asyncio.run(main())
