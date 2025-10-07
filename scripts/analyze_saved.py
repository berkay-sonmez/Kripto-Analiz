"""
Kaydedilmiş Verileri Analiz Et
Rate limit problemi olmadan mevcut verileri kullanır
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers.technical_analyzer import TechnicalAnalyzer
from src.utils.data_manager import DataManager
from src.config.my_watchlist import MY_WATCHLIST


def analyze_saved_data():
    """Kaydedilmiş verileri watchlist ile karşılaştır"""
    
    print("=" * 80)
    print("📊 KAYDEDİLMİŞ VERİLERDEN WATCHLIST ANALİZİ")
    print("=" * 80)
    print()
    
    # Veri yöneticisi
    data_manager = DataManager()
    analyzer = TechnicalAnalyzer()
    
    # En son verileri yükle
    print("📂 En son kaydedilen veriler yükleniyor...\n")
    all_coins = data_manager.load_latest_coins()
    
    if not all_coins:
        print("❌ Kaydedilmiş veri bulunamadı!")
        print("\n💡 Önce veri çekmek için:")
        print("   python scripts\\fetch_coins.py")
        print("\n   (Not: Şu anda TradingView rate limit nedeniyle veri çekme")
        print("   çalışmayabilir. 10-15 dakika sonra tekrar deneyin.)\n")
        return
    
    print(f"✅ Toplam {len(all_coins)} coin verisi yüklendi\n")
    
    # Watchlist'teki coinleri filtrele
    watchlist_coins = [c for c in all_coins if c['symbol'] in MY_WATCHLIST]
    
    print(f"📋 Watchlist'inizde: {len(MY_WATCHLIST)} coin")
    print(f"✅ Mevcut veriler: {len(watchlist_coins)} coin")
    
    # Eksik coinleri göster
    available_symbols = [c['symbol'] for c in watchlist_coins]
    missing = [s for s in MY_WATCHLIST if s not in available_symbols]
    
    if missing:
        print(f"⚠️  Verisi olmayan coinler: {', '.join(missing)}")
    
    print()
    
    if not watchlist_coins:
        print("❌ Watchlist'inizdeki coinler için veri bulunamadı!")
        print("\n💡 Watchlist'inizi güncellemek için:")
        print("   notepad src\\config\\my_watchlist.py\n")
        return
    
    # Analiz yap
    print("🔍 Teknik analiz yapılıyor...\n")
    signals = analyzer.analyze_batch(watchlist_coins)
    
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
            print(f"{icon} {signal['symbol']:8} | ${signal['price']:12,.2f} | "
                  f"RSI: {signal.get('rsi', 0):5.1f} | {signal['action']}")
            print(f"   └─ {signal['reason']}")
            print()
    
    # Detaylı tablo
    print("📋 WATCHLIST DETAYI:")
    print("=" * 80)
    print(f"{'COIN':8} | {'FİYAT':>14} | {'DEĞİŞİM':>8} | {'RSI':>6} | {'AKSİYON':8} | {'ÖNERI':12}")
    print("-" * 80)
    
    for signal in sorted(signals, key=lambda x: x['symbol']):
        coin_data = next((c for c in watchlist_coins if c['symbol'] == signal['symbol']), None)
        if not coin_data:
            continue
        
        change = coin_data.get('change_24h', 0)
        change_icon = "📈" if change > 0 else "📉"
        action_icon = "🟢" if signal['action'] == 'BUY' else "🔴" if signal['action'] == 'SELL' else "⚪"
        
        print(f"{signal['symbol']:8} | ${signal['price']:12,.2f} | "
              f"{change_icon} {change:+6.2f}% | {signal.get('rsi', 0):6.1f} | "
              f"{action_icon} {signal['action']:6} | {signal.get('recommendation', 'N/A'):12}")
    
    print()
    print("=" * 80)
    print("✅ Analiz Tamamlandı!")
    print("=" * 80)
    print()
    print("💡 Watchlist'inizi güncellemek için:")
    print("   notepad src\\config\\my_watchlist.py")
    print()
    print("💡 Yeni veri çekmek için (rate limit bittiğinde):")
    print("   python scripts\\fetch_coins.py")
    print()


if __name__ == "__main__":
    analyze_saved_data()
