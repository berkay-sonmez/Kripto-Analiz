"""
Teknik Analiz Modülü
RSI, MACD, Bollinger Bands ve diğer indikatörler
"""

from typing import List, Dict
import pandas as pd
from loguru import logger


class TechnicalAnalyzer:
    """Teknik analiz ve sinyal üretimi"""
    
    def __init__(self):
        """Teknik analiz modülünü başlat"""
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        logger.info("Teknik analiz modülü hazır")
    
    def analyze_coin(self, coin_data: Dict) -> Dict:
        """
        Gelişmiş teknik analiz - tüm indikatörler
        
        Args:
            coin_data: Detaylı coin verisi
            
        Returns:
            Kapsamlı analiz sonucu ve sinyal
        """
        symbol = coin_data.get("symbol", "UNKNOWN")
        price = coin_data.get("price", 0)
        
        # İndikatörler
        rsi = coin_data.get("rsi", 50)
        macd = coin_data.get("macd", 0)
        macd_signal = coin_data.get("macd_signal", 0)
        macd_histogram = coin_data.get("macd_histogram", 0)
        
        stoch_k = coin_data.get("stoch_k", 50)
        stoch_d = coin_data.get("stoch_d", 50)
        
        bb_upper = coin_data.get("bb_upper", 0)
        bb_lower = coin_data.get("bb_lower", 0)
        bb_middle = coin_data.get("bb_middle", 0)
        
        ema_20 = coin_data.get("ema_20", 0)
        ema_50 = coin_data.get("ema_50", 0)
        sma_200 = coin_data.get("sma_200", 0)
        
        adx = coin_data.get("adx", 0)
        cci = coin_data.get("cci", 0)
        
        recommendation = coin_data.get("recommendation", "NEUTRAL")
        buy_signals = coin_data.get("buy_signals", 0)
        sell_signals = coin_data.get("sell_signals", 0)
        
        # Analiz skorları
        buy_score = 0
        sell_score = 0
        reasons = []
        
        # 1. RSI Analizi
        if rsi < self.rsi_oversold:
            buy_score += 2
            reasons.append(f"RSI aşırı satım ({rsi:.1f})")
        elif rsi < 40:
            buy_score += 1
            reasons.append(f"RSI düşük ({rsi:.1f})")
        elif rsi > self.rsi_overbought:
            sell_score += 2
            reasons.append(f"RSI aşırı alım ({rsi:.1f})")
        elif rsi > 60:
            sell_score += 1
            reasons.append(f"RSI yüksek ({rsi:.1f})")
        
        # 2. MACD Analizi
        if macd > macd_signal and macd_histogram > 0:
            buy_score += 2
            reasons.append("MACD yükseliş geçişi")
        elif macd < macd_signal and macd_histogram < 0:
            sell_score += 2
            reasons.append("MACD düşüş geçişi")
        
        # 3. Stochastic Analizi
        if stoch_k < 20 and stoch_d < 20:
            buy_score += 1
            reasons.append(f"Stochastic aşırı satım ({stoch_k:.1f})")
        elif stoch_k > 80 and stoch_d > 80:
            sell_score += 1
            reasons.append(f"Stochastic aşırı alım ({stoch_k:.1f})")
        
        # 4. Bollinger Bands Analizi
        if price > 0 and bb_lower > 0 and bb_upper > 0:
            if price <= bb_lower * 1.01:  # Alt banda yakın
                buy_score += 1
                reasons.append("Bollinger alt bandında")
            elif price >= bb_upper * 0.99:  # Üst banda yakın
                sell_score += 1
                reasons.append("Bollinger üst bandında")
        
        # 5. Moving Average Analizi
        ma_trend = "NEUTRAL"
        if ema_20 > 0 and ema_50 > 0:
            if price > ema_20 > ema_50:
                buy_score += 1
                ma_trend = "BULLISH"
                reasons.append("EMA yükseliş trendi")
            elif price < ema_20 < ema_50:
                sell_score += 1
                ma_trend = "BEARISH"
                reasons.append("EMA düşüş trendi")
        
        # 6. ADX - Trend Gücü
        trend_strength = "WEAK"
        if adx > 25:
            trend_strength = "STRONG"
            if buy_score > sell_score:
                reasons.append(f"Güçlü yükseliş trendi (ADX: {adx:.1f})")
            elif sell_score > buy_score:
                reasons.append(f"Güçlü düşüş trendi (ADX: {adx:.1f})")
        elif adx < 20:
            trend_strength = "WEAK"
        
        # 7. CCI Analizi
        if cci < -100:
            buy_score += 1
            reasons.append(f"CCI aşırı satım ({cci:.1f})")
        elif cci > 100:
            sell_score += 1
            reasons.append(f"CCI aşırı alım ({cci:.1f})")
        
        # 8. TradingView Genel Önerisi
        if recommendation == "STRONG_BUY":
            buy_score += 3
            reasons.append("TV: Güçlü AL")
        elif recommendation == "BUY":
            buy_score += 2
            reasons.append("TV: AL")
        elif recommendation == "STRONG_SELL":
            sell_score += 3
            reasons.append("TV: Güçlü SAT")
        elif recommendation == "SELL":
            sell_score += 2
            reasons.append("TV: SAT")
        
        # 9. Sinyal Dengesi
        if buy_signals > sell_signals + 5:
            buy_score += 1
            reasons.append(f"Güçlü alım baskısı ({buy_signals}/{sell_signals})")
        elif sell_signals > buy_signals + 5:
            sell_score += 1
            reasons.append(f"Güçlü satış baskısı ({sell_signals}/{buy_signals})")
        
        # Nihai Karar
        action = "HOLD"
        signal_strength = "WEAK"
        confidence = 0
        
        if buy_score > sell_score + 2:
            action = "BUY"
            confidence = min(buy_score * 10, 100)
            if buy_score >= 8:
                signal_strength = "STRONG"
            elif buy_score >= 5:
                signal_strength = "MEDIUM"
        elif sell_score > buy_score + 2:
            action = "SELL"
            confidence = min(sell_score * 10, 100)
            if sell_score >= 8:
                signal_strength = "STRONG"
            elif sell_score >= 5:
                signal_strength = "MEDIUM"
        else:
            action = "HOLD"
            signal_strength = "NEUTRAL"
            confidence = 50
        
        return {
            "symbol": symbol,
            "action": action,
            "strength": signal_strength,
            "confidence": confidence,
            "buy_score": buy_score,
            "sell_score": sell_score,
            "reason": " | ".join(reasons[:5]) if reasons else "Belirgin sinyal yok",
            "all_reasons": reasons,
            
            # Detaylı indikatör değerleri
            "indicators": {
                "rsi": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "stoch_k": stoch_k,
                "stoch_d": stoch_d,
                "adx": adx,
                "cci": cci,
                "ma_trend": ma_trend,
                "trend_strength": trend_strength
            },
            
            "price": price,
            "volume": coin_data.get("volume", 0),
            "recommendation": recommendation
        }
    
    def analyze_batch(self, coins: List[Dict]) -> List[Dict]:
        """
        Birden fazla coin için toplu analiz
        
        Args:
            coins: Coin verileri listesi
            
        Returns:
            Analiz sonuçları listesi
        """
        results = []
        
        for coin in coins:
            try:
                result = self.analyze_coin(coin)
                results.append(result)
            except Exception as e:
                logger.error(f"❌ {coin.get('symbol')} analiz hatası: {e}")
        
        return results
    
    def filter_signals(self, signals: List[Dict], action: str = None, 
                      strength: str = None) -> List[Dict]:
        """
        Sinyalleri filtrele
        
        Args:
            signals: Sinyal listesi
            action: Aksiyon türü (BUY/SELL/HOLD)
            strength: Sinyal gücü (STRONG/WEAK/NEUTRAL)
            
        Returns:
            Filtrelenmiş sinyaller
        """
        filtered = signals
        
        if action:
            filtered = [s for s in filtered if s['action'] == action]
        
        if strength:
            filtered = [s for s in filtered if s['strength'] == strength]
        
        return filtered
