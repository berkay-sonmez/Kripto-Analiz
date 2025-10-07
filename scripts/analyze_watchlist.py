"""
Kişisel Watchlist Analizi
TradingView'deki izleme listenizdeki coinleri analiz eder
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.tradingview.tv_client import TradingViewClient
from src.analyzers.technical_analyzer import TechnicalAnalyzer
from src.utils.data_manager import DataManager
from src.config.my_watchlist import MY_WATCHLIST, DEFAULT_EXCHANGE

load_dotenv()


async def analyze_my_watchlist():
    """Kişisel watchlist'i analiz et"""
    
    print("=" * 80)
    print("📋 KİŞİSEL WATCHLIST ANALİZİ")
    print("=" * 80)
    print()
    
    # İzleme listesini göster
    print(f"📊 İzleme Listenizdeki Coinler ({len(MY_WATCHLIST)} adet):")
    print("-" * 80)
    for i, symbol in enumerate(MY_WATCHLIST, 1):
        print(f"{i:2}. {symbol}")
    print()
    
    # Onay al
    print("Bu coinleri analiz etmek istiyor musunuz?")
    print("Evet için Enter'a basın, hayır için 'n' yazıp Enter'a basın...")
    
    # Client oluştur
    tv_client = TradingViewClient()
    analyzer = TechnicalAnalyzer()
    data_manager = DataManager()
    
    print("\n🔍 Veriler çekiliyor...\n")
    
    # Watchlist'teki coinleri çek
    coins = await tv_client.fetch_all_altcoins(symbols=MY_WATCHLIST)
    
    if not coins:
        print("❌ Veri çekilemedi!")
        return
    
    print(f"✅ {len(coins)}/{len(MY_WATCHLIST)} coin verisi çekildi\n")
    
    # Analiz yap
    print("🔍 Teknik analiz yapılıyor...\n")
    signals = analyzer.analyze_batch(coins)
    
    # Sonuçları kategorize et
    buy_signals = [s for s in signals if s['action'] == 'BUY']
    sell_signals = [s for s in signals if s['action'] == 'SELL']
    hold_signals = [s for s in signals if s['action'] == 'HOLD']
    strong_signals = [s for s in signals if s['strength'] == 'STRONG']
    
    # Özet
    print("=" * 80)
    print("📊 ANALİZ ÖZETİ")
    print("=" * 80)
    print()
    print(f"🟢 AL Sinyalleri:    {len(buy_signals):2} coin")
    print(f"🔴 SAT Sinyalleri:   {len(sell_signals):2} coin")
    print(f"⚪ TUT Sinyalleri:   {len(hold_signals):2} coin")
    print(f"💪 Güçlü Sinyaller:  {len(strong_signals):2} coin")
    print()
    
    # Güçlü AL sinyalleri
    strong_buys = [s for s in strong_signals if s['action'] == 'BUY']
    if strong_buys:
        print("🎯 GÜÇLÜ AL SİNYALLERİ:")
        print("=" * 80)
        for signal in strong_buys:
            print(f"🟢 {signal['symbol']:8} | ${signal['price']:12,.2f} | RSI: {signal['rsi']:5.1f}")
            print(f"   └─ {signal['reason']}")
            print()
    
    # Güçlü SAT sinyalleri
    strong_sells = [s for s in strong_signals if s['action'] == 'SELL']
    if strong_sells:
        print("⚠️  GÜÇLÜ SAT SİNYALLERİ:")
        print("=" * 80)
        for signal in strong_sells:
            print(f"🔴 {signal['symbol']:8} | ${signal['price']:12,.2f} | RSI: {signal['rsi']:5.1f}")
            print(f"   └─ {signal['reason']}")
            print()
    
    # Detaylı tablo
    print("📋 DETAYLI TABLO:")
    print("=" * 80)
    print(f"{'COIN':8} | {'FİYAT':>14} | {'DEĞİŞİM':>8} | {'RSI':>6} | {'AKSİYON':8} | {'GÜÇ':8}")
    print("-" * 80)
    
    # Sinyalleri sırala: önce güçlü AL, sonra AL, TUT, SAT, güçlü SAT
    signal_order = {'BUY': 1, 'HOLD': 2, 'SELL': 3}
    strength_order = {'STRONG': 0, 'NEUTRAL': 1, 'WEAK': 2}
    
    sorted_signals = sorted(signals, 
                          key=lambda x: (signal_order.get(x['action'], 4), 
                                       strength_order.get(x['strength'], 3)))
    
    for signal in sorted_signals:
        coin_data = next((c for c in coins if c['symbol'] == signal['symbol']), None)
        if not coin_data:
            continue
        
        change = coin_data.get('change_24h', 0)
        change_icon = "📈" if change > 0 else "📉"
        
        action_icon = "🟢" if signal['action'] == 'BUY' else "🔴" if signal['action'] == 'SELL' else "⚪"
        strength_icon = "💪" if signal['strength'] == 'STRONG' else "  "
        
        rsi_value = signal.get('rsi', 0)
        
        print(f"{signal['symbol']:8} | ${signal['price']:12,.2f} | "
              f"{change_icon} {change:+6.2f}% | {rsi_value:6.1f} | "
              f"{action_icon} {signal['action']:6} | {strength_icon}{signal['strength']:6}")
    
    print()
    
    # En çok değişenler
    print("🔥 EN ÇOK HAREKETLİLER:")
    print("=" * 80)
    movers = tv_client.get_top_movers(coins, limit=5)
    
    print("\n📈 En Çok Yükselenler:")
    for coin in movers['top_gainers']:
        print(f"  • {coin['symbol']:8} | ${coin['price']:12,.2f} | +{coin['change_24h']:.2f}%")
    
    print("\n📉 En Çok Düşenler:")
    for coin in movers['top_losers']:
        print(f"  • {coin['symbol']:8} | ${coin['price']:12,.2f} | {coin['change_24h']:.2f}%")
    
    print()
    
    # Verileri kaydet
    print("💾 Veriler kaydediliyor...")
    data_manager.save_coins(coins, filename="watchlist_latest.json")
    data_manager.save_signals(signals, filename="watchlist_signals_latest.json")
    data_manager.export_to_csv(coins, filename="watchlist_latest.csv")
    
    print("✅ Veriler data/ klasörüne kaydedildi!")
    print()
    
    print("=" * 80)
    print("✅ Analiz Tamamlandı!")
    print("=" * 80)
    print()
    print("💡 İpucu: src/config/my_watchlist.py dosyasını düzenleyerek")
    print("   izleme listenize coin ekleyebilir veya çıkarabilirsiniz.")
    print()


if __name__ == "__main__":
    asyncio.run(analyze_my_watchlist())
