"""
Yoğun Aktivite Tespiti Test Scripti
Bir coinde çok sinyal geldiğinde özel alert vermeyi test eder
"""
from datetime import datetime, timedelta
from collections import defaultdict
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

# Simüle edilmiş bot özellikleri
class MockBot:
    def __init__(self):
        self.signal_history = defaultdict(list)
        self.high_activity_threshold = 5  # 30 dakikada 5+ sinyal
        self.activity_window_minutes = 30
        self.high_activity_alerted = {}
    
    def check_high_activity(self, symbol: str) -> bool:
        """Yoğunluk kontrolü"""
        now = datetime.now()
        history = self.signal_history[symbol]
        
        window_start = now - timedelta(minutes=self.activity_window_minutes)
        recent_signals = [
            s for s in history 
            if s.get('time') and datetime.fromisoformat(s['time']) >= window_start
        ]
        
        signal_count = len(recent_signals)
        
        if signal_count >= self.high_activity_threshold:
            last_activity_alert = self.high_activity_alerted.get(symbol)
            if last_activity_alert:
                minutes_since = (now - last_activity_alert).total_seconds() / 60
                if minutes_since < 10:
                    return False
            
            self.high_activity_alerted[symbol] = now
            
            longs = sum(1 for s in recent_signals if s.get('signal_type') == 'LONG')
            shorts = sum(1 for s in recent_signals if s.get('signal_type') == 'SHORT')
            direction = "LONG" if longs > shorts else "SHORT" if shorts > longs else "MİXED"
            
            alert_msg = f"""
{'🔥'*80}
{'⚠️ '*40}
║ 
║ 🚨🚨🚨 YOĞUN AKTİVİTE TESPİT EDİLDİ! 🚨🚨🚨
║ 
║ 💎 Coin: {symbol}
║ 📊 Sinyal Sayısı: {signal_count} sinyal / {self.activity_window_minutes} dakika
║ 📈 Yön: {longs} LONG / {shorts} SHORT → {direction} dominant
║ 
║ 💡 Analiz: Bu coin ÇOK HAREKETLÜ! Büyük bir hareket başlıyor olabilir.
║          {self.activity_window_minutes} dakikada {signal_count} whale sinyali geldi!
║ 
║ 🎯 Öneri: Bu coini ŞİMDİ detaylı analiz et ve pozisyon açmayı düşün!
║          Trend {direction} yönünde güçlü görünüyor.
║ 
{'⚠️ '*40}
{'🔥'*80}
"""
            logger.critical(alert_msg)
            return True
        
        return False

def test_scenario_1():
    """Senaryo 1: Normal aktivite - alert olmamalı"""
    logger.info("\n" + "="*80)
    logger.info("TEST 1: Normal Aktivite (30 dakikada 3 sinyal)")
    logger.info("="*80)
    
    bot = MockBot()
    now = datetime.now()
    
    # BTCUSDT için 3 sinyal (yoğunluk yok)
    for i in range(3):
        bot.signal_history['BTCUSDT'].append({
            'time': (now - timedelta(minutes=i*10)).isoformat(),
            'signal_type': 'LONG',
            'strength': 'Medium'
        })
    
    result = bot.check_high_activity('BTCUSDT')
    logger.info(f"Sonuç: {'❌ Alert VERİLMEDİ (Doğru!)' if not result else '⚠️ Alert verildi (YANLIŞ!)'}")

def test_scenario_2():
    """Senaryo 2: Yoğun aktivite - alert olmalı"""
    logger.info("\n" + "="*80)
    logger.info("TEST 2: Yoğun Aktivite (30 dakikada 7 sinyal - LONG dominant)")
    logger.info("="*80)
    
    bot = MockBot()
    now = datetime.now()
    
    # ETHUSDT için 7 sinyal (yoğun!)
    for i in range(7):
        bot.signal_history['ETHUSDT'].append({
            'time': (now - timedelta(minutes=i*4)).isoformat(),
            'signal_type': 'LONG' if i < 5 else 'SHORT',  # 5 LONG, 2 SHORT
            'strength': 'Medium'
        })
    
    result = bot.check_high_activity('ETHUSDT')
    logger.info(f"Sonuç: {'✅ Alert VERİLDİ (Doğru!)' if result else '❌ Alert verilmedi (YANLIŞ!)'}")

def test_scenario_3():
    """Senaryo 3: Çok yoğun SHORT aktivitesi"""
    logger.info("\n" + "="*80)
    logger.info("TEST 3: Çok Yoğun SHORT Aktivitesi (20 dakikada 8 sinyal)")
    logger.info("="*80)
    
    bot = MockBot()
    now = datetime.now()
    
    # SOLUSDT için 8 SHORT sinyal (çok yoğun!)
    for i in range(8):
        bot.signal_history['SOLUSDT'].append({
            'time': (now - timedelta(minutes=i*2.5)).isoformat(),
            'signal_type': 'SHORT',  # Hepsi SHORT
            'strength': 'High' if i < 2 else 'Medium'
        })
    
    result = bot.check_high_activity('SOLUSDT')
    logger.info(f"Sonuç: {'✅ Alert VERİLDİ (Doğru!)' if result else '❌ Alert verilmedi (YANLIŞ!)'}")

def test_scenario_4():
    """Senaryo 4: Mixed sinyaller ama yine de yoğun"""
    logger.info("\n" + "="*80)
    logger.info("TEST 4: Mixed Yoğunluk (25 dakikada 6 sinyal - 3 LONG, 3 SHORT)")
    logger.info("="*80)
    
    bot = MockBot()
    now = datetime.now()
    
    # BNBUSDT için 6 mixed sinyal
    for i in range(6):
        bot.signal_history['BNBUSDT'].append({
            'time': (now - timedelta(minutes=i*4)).isoformat(),
            'signal_type': 'LONG' if i % 2 == 0 else 'SHORT',
            'strength': 'Medium'
        })
    
    result = bot.check_high_activity('BNBUSDT')
    logger.info(f"Sonuç: {'✅ Alert VERİLDİ (Doğru!)' if result else '❌ Alert verilmedi (YANLIŞ!)'}")

if __name__ == "__main__":
    logger.info("🧪 Yoğun Aktivite Tespiti - Test Başlıyor...")
    
    test_scenario_1()  # Normal → Alert yok
    test_scenario_2()  # Yoğun LONG → Alert var
    test_scenario_3()  # Çok yoğun SHORT → Alert var
    test_scenario_4()  # Mixed yoğun → Alert var
    
    logger.info("\n" + "="*80)
    logger.info("✅ Tüm testler tamamlandı!")
    logger.info("="*80)
