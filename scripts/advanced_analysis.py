"""
Gelişmiş Analiz Script
TradingView hesabı ile detaylı indikatör analizi
Multi-timeframe analiz desteği
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from tradingview_ta import Interval
from src.tradingview.tv_client import TradingViewClient
from src.analyzers.technical_analyzer import TechnicalAnalyzer
from src.utils.data_manager import DataManager

load_dotenv()


async def analyze_single_coin(symbol: str):
    """Tek bir coin için detaylı multi-timeframe analiz"""
    print(f"\n{'='*80}")
    print(f"🔍 {symbol} - DETAYLI ANALİZ")
    print(f"{'='*80}\n")
    
    tv_client = TradingViewClient()
    analyzer = TechnicalAnalyzer()
    
    # Multi-timeframe analizi
    result = await tv_client.fetch_multi_timeframe(symbol)
    
    if not result or not result.get("timeframes"):
        print(f"❌ {symbol} için veri çekilemedi!")
        return
    
    timeframes = result["timeframes"]
    summary = result["summary"]
    
    print(f"📊 GENEL GÖRÜNÜM")
    print(f"-" * 80)
    print(f"Trend: {summary['trend']}")
    print(f"Yükseliş Sinyali: {summary['bullish_count']}/4 timeframe")
    print(f"Düşüş Sinyali: {summary['bearish_count']}/4 timeframe")
    print(f"Nötr: {summary['neutral_count']}/4 timeframe")
    
    # Her timeframe için detaylı analiz
    for tf_name, tf_data in timeframes.items():
        print(f"\n⏱️  {tf_name.upper()}")
        print(f"-" * 80)
        
        analysis = analyzer.analyze_coin(tf_data)
        
        print(f"Fiyat: ${tf_data['price']:,.2f}")
        print(f"Aksiyon: {analysis['action']} ({analysis['strength']}) - Güven: %{analysis['confidence']}")
        print(f"Skor: AL={analysis['buy_score']} / SAT={analysis['sell_score']}")
        
        print(f"\nİndikatörler:")
        ind = analysis['indicators']
        print(f"  • RSI: {ind['rsi']:.1f}")
        print(f"  • MACD: {ind['macd']:.4f} (Signal: {ind['macd_signal']:.4f})")
        print(f"  • Stochastic: K={ind['stoch_k']:.1f}, D={ind['stoch_d']:.1f}")
        print(f"  • ADX: {ind['adx']:.1f} ({ind['trend_strength']} trend)")
        print(f"  • CCI: {ind['cci']:.1f}")
        print(f"  • MA Trend: {ind['ma_trend']}")
        
        print(f"\nSebepler:")
        for i, reason in enumerate(analysis.get('all_reasons', [])[:5], 1):
            print(f"  {i}. {reason}")
    
    print(f"\n{'='*80}\n")


async def analyze_all_with_indicators():
    """Tüm coinler için gelişmiş indikatör analizi"""
    print("🚀 GELİŞMİŞ İNDİKATÖR ANALİZİ BAŞLATILIYOR...\n")
    
    tv_client = TradingViewClient()
    analyzer = TechnicalAnalyzer()
    data_manager = DataManager()
    
    # Verileri çek (15 dakikalık interval)
    print("📥 Altcoin verileri çekiliyor (15 dakikalık interval)...\n")
    coins = await tv_client.fetch_all_altcoins(interval=Interval.INTERVAL_15_MINUTES)
    
    if not coins:
        print("❌ Veri çekilemedi!")
        return
    
    print(f"✅ {len(coins)} coin verisi çekildi\n")
    
    # Analiz yap
    print("🔍 Detaylı teknik analiz yapılıyor...\n")
    signals = analyzer.analyze_batch(coins)
    
    # Güçlü sinyalleri filtrele
    strong_buy = [s for s in signals if s['action'] == 'BUY' and s['strength'] in ['STRONG', 'MEDIUM']]
    strong_sell = [s for s in signals if s['action'] == 'SELL' and s['strength'] in ['STRONG', 'MEDIUM']]
    
    # Güvene göre sırala
    strong_buy.sort(key=lambda x: x.get('confidence', 0), reverse=True)
    strong_sell.sort(key=lambda x: x.get('confidence', 0), reverse=True)
    
    print(f"{'='*100}")
    print(f"🟢 GÜÇLÜ ALIM SİNYALLERİ ({len(strong_buy)} coin)")
    print(f"{'='*100}\n")
    
    for signal in strong_buy[:10]:
        print(f"{signal['symbol']:8} | {signal['strength']:8} | Güven: %{signal['confidence']:3} | "
              f"Skor: {signal['buy_score']:2} | RSI: {signal['indicators']['rsi']:5.1f}")
        print(f"         → {signal['reason']}")
        print()
    
    print(f"{'='*100}")
    print(f"🔴 GÜÇLÜ SATIŞ SİNYALLERİ ({len(strong_sell)} coin)")
    print(f"{'='*100}\n")
    
    for signal in strong_sell[:10]:
        print(f"{signal['symbol']:8} | {signal['strength']:8} | Güven: %{signal['confidence']:3} | "
              f"Skor: {signal['sell_score']:2} | RSI: {signal['indicators']['rsi']:5.1f}")
        print(f"         → {signal['reason']}")
        print()
    
    # Verileri kaydet
    data_manager.save_coins(coins, "detailed_coins_15m.json")
    data_manager.save_signals(signals, "detailed_signals_15m.json")
    
    print("✅ Detaylı analiz verileri kaydedildi!")


async def main():
    """Ana fonksiyon"""
    print("\n" + "="*100)
    print("🎯 GELİŞMİŞ KRİPTO ANALİZ ARACI")
    print("="*100 + "\n")
    
    print("Ne yapmak istersiniz?")
    print("1. Tüm coinleri analiz et (detaylı indikatörlerle)")
    print("2. Tek bir coin için multi-timeframe analiz (15m, 1h, 4h, 1d)")
    print()
    
    choice = input("Seçiminiz (1/2): ").strip()
    
    if choice == "1":
        await analyze_all_with_indicators()
    elif choice == "2":
        symbol = input("Coin sembolü (örn: ETH, BTC, SOL): ").strip().upper()
        if symbol:
            await analyze_single_coin(symbol)
        else:
            print("❌ Geçersiz sembol!")
    else:
        print("❌ Geçersiz seçim!")


if __name__ == "__main__":
    asyncio.run(main())
