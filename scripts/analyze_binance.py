"""
Binance ile Watchlist Analizi
TradingView rate limit sorunu olmadan çalışır!
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.binance.binance_client import BinanceClient
from src.analyzers.technical_analyzer import TechnicalAnalyzer
from src.utils.data_manager import DataManager
from src.config.my_watchlist import MY_WATCHLIST


async def analyze_with_binance():
    """Binance API ile watchlist analizi"""
    
    print("=" * 80)
    print("🚀 BINANCE API İLE WATCHLIST ANALİZİ")
    print("=" * 80)
    print()
    print("✅ Avantajlar:")
    print("   • Rate limit yok!")
    print("   • Çok hızlı veri çekme")
    print("   • Tüm indikatörler (RSI, MACD, BB, EMA, SMA, Stochastic)")
    print("   • Binance'ın resmi API'si")
    print()
    print("=" * 80)
    print()
    
    print(f"📋 İzleme Listenizdeki Coinler: {len(MY_WATCHLIST)} adet\n")
    
    # Binance client oluştur
    binance = BinanceClient()
    analyzer = TechnicalAnalyzer()
    data_manager = DataManager()
    
    try:
        print("⚡ Veriler çekiliyor (çok hızlı!)...\n")
        
        # Tüm coinleri paralel çek
        coins = await binance.fetch_multiple_coins(MY_WATCHLIST, timeframe='15m')
        
        if not coins:
            print("❌ Hiç veri çekilemedi!")
            return
        
        print(f"\n✅ {len(coins)}/{len(MY_WATCHLIST)} coin verisi çekildi\n")
        
        # Eksik coinleri göster
        successful_symbols = [c['symbol'] for c in coins]
        missing = [s for s in MY_WATCHLIST if s not in successful_symbols]
        
        if missing:
            print(f"⚠️  Binance'de bulunamayan coinler: {', '.join(missing)}\n")
        
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
        
        # Güçlü sinyaller
        if strong_signals:
            print("🎯 GÜÇLÜ SİNYALLER:")
            print("=" * 80)
            for signal in strong_signals:
                icon = "🟢" if signal['action'] == 'BUY' else "🔴"
                print(f"{icon} {signal['symbol']:8} | ${signal['price']:12,.4f} | "
                      f"RSI: {signal.get('rsi', 0):5.1f} | {signal['action']}")
                print(f"   └─ {signal['reason']}")
                print()
        
        # Detaylı tablo
        print("📋 DETAYLI İNDİKATÖR TABLOSU:")
        print("=" * 80)
        print(f"{'COIN':8} | {'FİYAT':>12} | {'DEĞ%':>6} | {'RSI':>5} | "
              f"{'MACD':>7} | {'EMA9>21':^7} | {'AKSİYON':8}")
        print("-" * 80)
        
        for signal in sorted(signals, key=lambda x: x['symbol']):
            coin_data = next((c for c in coins if c['symbol'] == signal['symbol']), None)
            if not coin_data:
                continue
            
            change = coin_data.get('change_24h', 0)
            rsi = signal.get('rsi', 0)
            macd_hist = coin_data.get('macd_hist', 0)
            ema_9 = coin_data.get('ema_9', 0)
            ema_21 = coin_data.get('ema_21', 0)
            
            change_icon = "📈" if change > 0 else "📉"
            action_icon = "🟢" if signal['action'] == 'BUY' else "🔴" if signal['action'] == 'SELL' else "⚪"
            ema_cross = "✅" if ema_9 > ema_21 else "❌"
            
            print(f"{signal['symbol']:8} | ${signal['price']:12,.4f} | "
                  f"{change:+6.2f} | {rsi:5.1f} | "
                  f"{macd_hist:+7.2f} | {ema_cross:^7} | "
                  f"{action_icon} {signal['action']:6}")
        
        print()
        
        # En iyi fırsatlar
        print("🎯 EN İYİ FIRSATLAR (Düşük RSI + AL sinyali):")
        print("=" * 80)
        
        opportunities = [s for s in signals if s.get('rsi', 100) < 40 and s['action'] == 'BUY']
        opportunities = sorted(opportunities, key=lambda x: x.get('rsi', 100))
        
        if opportunities:
            for opp in opportunities[:5]:
                coin_data = next((c for c in coins if c['symbol'] == opp['symbol']), None)
                if coin_data:
                    print(f"🟢 {opp['symbol']:8} | ${opp['price']:12,.4f} | "
                          f"RSI: {opp.get('rsi', 0):5.1f} | MACD: {coin_data.get('macd_hist', 0):+7.2f}")
            print()
        else:
            print("   Şu anda uygun fırsat bulunamadı.\n")
        
        # En yüksek risk (Aşırı alım + SAT sinyali)
        print("⚠️  YÜKSEK RİSK (Aşırı Alım + SAT sinyali):")
        print("=" * 80)
        
        risks = [s for s in signals if s.get('rsi', 0) > 60 and s['action'] == 'SELL']
        risks = sorted(risks, key=lambda x: x.get('rsi', 0), reverse=True)
        
        if risks:
            for risk in risks[:5]:
                coin_data = next((c for c in coins if c['symbol'] == risk['symbol']), None)
                if coin_data:
                    print(f"🔴 {risk['symbol']:8} | ${risk['price']:12,.4f} | "
                          f"RSI: {risk.get('rsi', 0):5.1f} | MACD: {coin_data.get('macd_hist', 0):+7.2f}")
            print()
        else:
            print("   Şu anda yüksek riskli coin bulunamadı.\n")
        
        # Verileri kaydet
        print("💾 Veriler kaydediliyor...")
        data_manager.save_coins(coins, filename="binance_watchlist_latest.json")
        data_manager.save_signals(signals, filename="binance_signals_latest.json")
        data_manager.export_to_csv(coins, filename="binance_watchlist_latest.csv")
        
        print("✅ Veriler data/ klasörüne kaydedildi!")
        print()
        
        print("=" * 80)
        print("✅ Analiz Tamamlandı!")
        print("=" * 80)
        print()
        print("💡 Bu script her zaman rate limit olmadan çalışır!")
        print("   Komut: python scripts\\analyze_binance.py")
        print()
        
    finally:
        await binance.close()


if __name__ == "__main__":
    asyncio.run(analyze_with_binance())
