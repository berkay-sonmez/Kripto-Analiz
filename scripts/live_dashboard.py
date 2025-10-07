"""
Gerçek Zamanlı Dashboard
Canlı fiyat takibi ve sinyal bildirimleri
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from tradingview_ta import Interval
from src.tradingview.tv_client import TradingViewClient
from src.analyzers.technical_analyzer import TechnicalAnalyzer

load_dotenv()


class CryptoDashboard:
    """Gerçek zamanlı kripto takip dashboard'u"""
    
    def __init__(self):
        self.tv_client = TradingViewClient()
        self.analyzer = TechnicalAnalyzer()
        self.previous_signals = {}
        self.update_interval = int(os.getenv("UPDATE_INTERVAL", 300))
    
    def clear_screen(self):
        """Ekranı temizle"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Dashboard başlığı"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("="*120)
        print(f"🎯 KRİPTO ANALİZ DASHBOARD - Canlı Takip".center(120))
        print(f"Son Güncelleme: {now}".center(120))
        print("="*120)
        print()
    
    def print_summary_table(self, signals: list):
        """Özet tablo yazdır"""
        # Aksiyonlara göre grupla
        buy_signals = [s for s in signals if s['action'] == 'BUY']
        sell_signals = [s for s in signals if s['action'] == 'SELL']
        hold_signals = [s for s in signals if s['action'] == 'HOLD']
        
        strong_buy = [s for s in buy_signals if s['strength'] in ['STRONG', 'MEDIUM']]
        strong_sell = [s for s in sell_signals if s['strength'] in ['STRONG', 'MEDIUM']]
        
        print(f"📊 GENEL DURUM")
        print("-"*120)
        print(f"Toplam: {len(signals)} coin | 🟢 AL: {len(buy_signals)} ({len(strong_buy)} güçlü) | "
              f"🔴 SAT: {len(sell_signals)} ({len(strong_sell)} güçlü) | ⚪ TUT: {len(hold_signals)}")
        print()
    
    def print_top_signals(self, signals: list, limit: int = 8):
        """En iyi sinyalleri göster"""
        # Güçlü alım sinyalleri
        strong_buy = [s for s in signals 
                     if s['action'] == 'BUY' and s['strength'] in ['STRONG', 'MEDIUM']]
        strong_buy.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        print(f"🟢 GÜÇLÜ ALIM SİNYALLERİ (Top {min(limit, len(strong_buy))})")
        print("-"*120)
        print(f"{'Symbol':<10} {'Fiyat':<15} {'RSI':<8} {'MACD':<10} {'Güven':<8} {'Güç':<10} {'Sebep':<50}")
        print("-"*120)
        
        for signal in strong_buy[:limit]:
            symbol = signal['symbol']
            price = signal['price']
            rsi = signal['indicators']['rsi']
            macd = signal['indicators']['macd']
            conf = signal['confidence']
            strength = signal['strength']
            reason = signal['reason'][:47] + "..." if len(signal['reason']) > 50 else signal['reason']
            
            # Yeni sinyal kontrolü
            new_tag = "🆕" if symbol not in self.previous_signals or \
                      self.previous_signals[symbol]['action'] != 'BUY' else "  "
            
            print(f"{new_tag}{symbol:<8} ${price:<13,.2f} {rsi:<7.1f} {macd:<9.4f} %{conf:<6} {strength:<10} {reason}")
        
        print()
        
        # Güçlü satış sinyalleri
        strong_sell = [s for s in signals 
                      if s['action'] == 'SELL' and s['strength'] in ['STRONG', 'MEDIUM']]
        strong_sell.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        print(f"🔴 GÜÇLÜ SATIŞ SİNYALLERİ (Top {min(limit, len(strong_sell))})")
        print("-"*120)
        print(f"{'Symbol':<10} {'Fiyat':<15} {'RSI':<8} {'MACD':<10} {'Güven':<8} {'Güç':<10} {'Sebep':<50}")
        print("-"*120)
        
        for signal in strong_sell[:limit]:
            symbol = signal['symbol']
            price = signal['price']
            rsi = signal['indicators']['rsi']
            macd = signal['indicators']['macd']
            conf = signal['confidence']
            strength = signal['strength']
            reason = signal['reason'][:47] + "..." if len(signal['reason']) > 50 else signal['reason']
            
            new_tag = "🆕" if symbol not in self.previous_signals or \
                      self.previous_signals[symbol]['action'] != 'SELL' else "  "
            
            print(f"{new_tag}{symbol:<8} ${price:<13,.2f} {rsi:<7.1f} {macd:<9.4f} %{conf:<6} {strength:<10} {reason}")
        
        print()
    
    def detect_signal_changes(self, new_signals: list):
        """Sinyal değişikliklerini tespit et"""
        changes = []
        
        for signal in new_signals:
            symbol = signal['symbol']
            action = signal['action']
            strength = signal['strength']
            
            if symbol in self.previous_signals:
                prev = self.previous_signals[symbol]
                
                # Aksiyon değişimi
                if prev['action'] != action and action != 'HOLD':
                    changes.append({
                        'symbol': symbol,
                        'type': 'ACTION_CHANGE',
                        'from': prev['action'],
                        'to': action,
                        'strength': strength,
                        'price': signal['price']
                    })
                
                # Güç artışı
                elif action == prev['action'] and strength == 'STRONG' and prev['strength'] != 'STRONG':
                    changes.append({
                        'symbol': symbol,
                        'type': 'STRENGTH_INCREASE',
                        'action': action,
                        'strength': strength,
                        'price': signal['price']
                    })
        
        return changes
    
    def print_changes(self, changes: list):
        """Değişiklikleri göster"""
        if not changes:
            return
        
        print(f"🔔 SİNYAL DEĞİŞİKLİKLERİ ({len(changes)})")
        print("-"*120)
        
        for change in changes:
            symbol = change['symbol']
            price = change['price']
            
            if change['type'] == 'ACTION_CHANGE':
                from_action = change['from']
                to_action = change['to']
                print(f"  • {symbol}: {from_action} → {to_action} (${price:,.2f}) - {change['strength']}")
            
            elif change['type'] == 'STRENGTH_INCREASE':
                action = change['action']
                print(f"  • {symbol}: {action} sinyali güçlendi → STRONG (${price:,.2f})")
        
        print()
    
    async def run(self):
        """Dashboard'u çalıştır"""
        print("🚀 Dashboard başlatılıyor...")
        print(f"⏱️  Güncelleme aralığı: {self.update_interval} saniye")
        print("⏹️  Durdurmak için Ctrl+C\n")
        
        await asyncio.sleep(2)
        
        while True:
            try:
                # Verileri çek
                coins = await self.tv_client.fetch_all_altcoins(
                    interval=Interval.INTERVAL_15_MINUTES
                )
                
                if not coins:
                    print("❌ Veri çekilemedi, tekrar deneniyor...")
                    await asyncio.sleep(30)
                    continue
                
                # Analiz yap
                signals = self.analyzer.analyze_batch(coins)
                
                # Değişiklikleri tespit et
                changes = self.detect_signal_changes(signals)
                
                # Ekranı güncelle
                self.clear_screen()
                self.print_header()
                self.print_summary_table(signals)
                self.print_changes(changes)
                self.print_top_signals(signals, limit=8)
                
                # Sinyalleri kaydet (değişiklik tespiti için)
                self.previous_signals = {s['symbol']: s for s in signals}
                
                print("-"*120)
                print(f"⏳ Sonraki güncelleme {self.update_interval} saniye sonra... (Ctrl+C ile dur)")
                
                # Bekle
                await asyncio.sleep(self.update_interval)
                
            except KeyboardInterrupt:
                print("\n\n⏹️  Dashboard durduruluyor...")
                break
            except Exception as e:
                print(f"\n❌ Hata: {e}")
                print("⏳ 60 saniye sonra tekrar denenecek...\n")
                await asyncio.sleep(60)


async def main():
    """Ana fonksiyon"""
    dashboard = CryptoDashboard()
    await dashboard.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard kapatıldı!")
