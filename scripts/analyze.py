"""
Analiz Script
Kaydedilmiş verileri analiz et
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers.technical_analyzer import TechnicalAnalyzer
from src.utils.data_manager import DataManager


def main():
    """Analiz yap"""
    print("🔍 Analiz başlatılıyor...\n")
    
    # Modülleri yükle
    data_manager = DataManager()
    analyzer = TechnicalAnalyzer()
    
    # En son verileri yükle
    coins = data_manager.load_latest_coins()
    
    if not coins:
        print("❌ Analiz edilecek veri yok! Önce fetch_coins.py çalıştırın.")
        return
    
    # Analiz yap
    signals = analyzer.analyze_batch(coins)
    
    # Sinyalleri filtrele
    buy_signals = analyzer.filter_signals(signals, action="BUY")
    sell_signals = analyzer.filter_signals(signals, action="SELL")
    strong_signals = analyzer.filter_signals(signals, strength="STRONG")
    
    # Sonuçları göster
    print(f"📊 Toplam {len(coins)} coin analiz edildi\n")
    
    print(f"🟢 AL Sinyalleri: {len(buy_signals)}")
    print(f"🔴 SAT Sinyalleri: {len(sell_signals)}")
    print(f"💪 Güçlü Sinyaller: {len(strong_signals)}\n")
    
    if strong_signals:
        print("🎯 Güçlü Sinyaller:")
        print("-" * 80)
        for signal in strong_signals:
            action_icon = "🟢" if signal['action'] == "BUY" else "🔴"
            print(f"{action_icon} {signal['symbol']:8} | {signal['action']:4} | {signal['reason']}")
    
    # Kaydet
    data_manager.save_signals(signals)
    print("\n✅ Sonuçlar data/ klasörüne kaydedildi!")


if __name__ == "__main__":
    main()
