"""
TradingView API İstemcisi
Altcoin verilerini çeker ve analiz için hazırlar
"""

import asyncio
from typing import List, Dict
from tradingview_ta import TA_Handler, Interval
from loguru import logger


class TradingViewClient:
    """TradingView veri çekme ve analiz client'ı"""
    
    # Popüler altcoinler (genişletilebilir)
    MAJOR_ALTCOINS = [
        "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE", "DOT", "MATIC", 
        "LTC", "AVAX", "LINK", "UNI", "ATOM", "XLM", "NEAR",
        "ALGO", "VET", "FIL", "HBAR", "APT", "ARB", "OP",
        "SAND", "MANA", "AXS", "IMX", "GRT", "ENJ", "CHZ",
        "AAVE", "MKR", "SNX", "CRV", "COMP", "SUSHI", "YFI"
    ]
    
    def __init__(self, username: str = None, password: str = None):
        """
        TradingView client başlat
        
        Args:
            username: TradingView kullanıcı adı (opsiyonel, public data için gerekli değil)
            password: TradingView şifre (opsiyonel)
        """
        self.username = username
        self.password = password
        logger.info(f"TradingView client başlatıldı")
    
    async def fetch_coin_data(self, symbol: str, exchange: str = "BINANCE", 
                            interval: Interval = Interval.INTERVAL_15_MINUTES) -> Dict:
        """
        Tek bir coin için detaylı veri ve indikatörler çek
        
        Args:
            symbol: Coin sembolü (örn: "BTCUSDT")
            exchange: Exchange adı
            interval: Zaman aralığı (15min, 1h, 4h, 1d)
            
        Returns:
            Detaylı coin verisi ve tüm indikatörler
        """
        try:
            # TradingView handler oluştur
            handler = TA_Handler(
                symbol=f"{symbol}USDT" if not symbol.endswith("USDT") else symbol,
                exchange=exchange,
                screener="crypto",
                interval=interval
            )
            
            # Analiz al
            analysis = handler.get_analysis()
            indicators = analysis.indicators
            
            # Detaylı indikatör verileri
            return {
                "symbol": symbol,
                "exchange": exchange,
                "interval": str(interval),
                
                # Fiyat ve Hacim
                "price": indicators.get("close", 0),
                "open": indicators.get("open", 0),
                "high": indicators.get("high", 0),
                "low": indicators.get("low", 0),
                "volume": indicators.get("volume", 0),
                "change_24h": indicators.get("change", 0),
                
                # RSI (Relative Strength Index)
                "rsi": indicators.get("RSI", 0),
                "rsi_7": indicators.get("RSI[1]", 0),
                
                # MACD (Moving Average Convergence Divergence)
                "macd": indicators.get("MACD.macd", 0),
                "macd_signal": indicators.get("MACD.signal", 0),
                "macd_histogram": indicators.get("MACD.macd", 0) - indicators.get("MACD.signal", 0),
                
                # Bollinger Bands
                "bb_upper": indicators.get("BB.upper", 0),
                "bb_middle": indicators.get("BB.middle", 0),
                "bb_lower": indicators.get("BB.lower", 0),
                
                # Stochastic
                "stoch_k": indicators.get("Stoch.K", 0),
                "stoch_d": indicators.get("Stoch.D", 0),
                
                # Moving Averages
                "ema_10": indicators.get("EMA10", 0),
                "ema_20": indicators.get("EMA20", 0),
                "ema_50": indicators.get("EMA50", 0),
                "ema_100": indicators.get("EMA100", 0),
                "ema_200": indicators.get("EMA200", 0),
                "sma_10": indicators.get("SMA10", 0),
                "sma_20": indicators.get("SMA20", 0),
                "sma_50": indicators.get("SMA50", 0),
                "sma_100": indicators.get("SMA100", 0),
                "sma_200": indicators.get("SMA200", 0),
                
                # ADX (Average Directional Index)
                "adx": indicators.get("ADX", 0),
                "adx_plus_di": indicators.get("ADX+DI", 0),
                "adx_minus_di": indicators.get("ADX-DI", 0),
                
                # CCI (Commodity Channel Index)
                "cci": indicators.get("CCI20", 0),
                
                # Momentum
                "momentum": indicators.get("Mom", 0),
                
                # ATR (Average True Range) - Volatilite
                "atr": indicators.get("ATR", 0),
                
                # Volume Weighted Average Price
                "vwap": indicators.get("VWMA", 0),
                
                # TradingView Önerileri
                "recommendation": analysis.summary.get("RECOMMENDATION", "NEUTRAL"),
                "buy_signals": analysis.summary.get("BUY", 0),
                "sell_signals": analysis.summary.get("SELL", 0),
                "neutral_signals": analysis.summary.get("NEUTRAL", 0),
                
                # Ham veriler (detaylı analiz için)
                "oscillators": analysis.oscillators,
                "moving_averages": analysis.moving_averages,
                "indicators": indicators
            }
            
        except Exception as e:
            logger.warning(f"❌ {symbol} verisi çekilemedi: {e}")
            return None
    
    async def fetch_all_altcoins(self, symbols: List[str] = None, 
                                interval: Interval = Interval.INTERVAL_15_MINUTES) -> List[Dict]:
        """
        Tüm altcoinlerin verilerini çek
        
        Args:
            symbols: Coin sembolleri listesi (None ise varsayılan liste kullanılır)
            interval: Zaman aralığı (15m, 1h, 4h, 1d)
            
        Returns:
            Coin verileri listesi
        """
        if symbols is None:
            symbols = self.MAJOR_ALTCOINS
        
        logger.info(f"📥 {len(symbols)} altcoin için veri çekiliyor... (Interval: {interval})")
        
        # Paralel veri çekme (rate limit için küçük delay)
        tasks = [self.fetch_coin_data(symbol, interval=interval) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        
        # Başarılı sonuçları filtrele
        coins = [r for r in results if r is not None]
        
        logger.info(f"✅ {len(coins)}/{len(symbols)} coin verisi başarıyla çekildi")
        return coins
    
    async def fetch_multi_timeframe(self, symbol: str, 
                                   intervals: List[Interval] = None) -> Dict:
        """
        Bir coin için birden fazla zaman diliminde veri çek
        
        Args:
            symbol: Coin sembolü
            intervals: Zaman dilimleri listesi
            
        Returns:
            Farklı timeframe'lerde coin verileri
        """
        if intervals is None:
            intervals = [
                Interval.INTERVAL_15_MINUTES,
                Interval.INTERVAL_1_HOUR,
                Interval.INTERVAL_4_HOURS,
                Interval.INTERVAL_1_DAY
            ]
        
        logger.info(f"📊 {symbol} için {len(intervals)} farklı timeframe verisi çekiliyor...")
        
        results = {}
        for interval in intervals:
            data = await self.fetch_coin_data(symbol, interval=interval)
            if data:
                interval_name = str(interval).split('.')[-1].lower()
                results[interval_name] = data
        
        return {
            "symbol": symbol,
            "timeframes": results,
            "summary": self._generate_multi_timeframe_summary(results)
        }
    
    def _generate_multi_timeframe_summary(self, timeframes: Dict) -> Dict:
        """
        Multi-timeframe analiz özeti oluştur
        
        Args:
            timeframes: Farklı timeframe verileri
            
        Returns:
            Özet analiz
        """
        summary = {
            "bullish_count": 0,
            "bearish_count": 0,
            "neutral_count": 0,
            "trend": "NEUTRAL"
        }
        
        for tf_name, tf_data in timeframes.items():
            rec = tf_data.get("recommendation", "NEUTRAL")
            if "BUY" in rec:
                summary["bullish_count"] += 1
            elif "SELL" in rec:
                summary["bearish_count"] += 1
            else:
                summary["neutral_count"] += 1
        
        # Genel trend
        if summary["bullish_count"] > summary["bearish_count"]:
            summary["trend"] = "BULLISH"
        elif summary["bearish_count"] > summary["bullish_count"]:
            summary["trend"] = "BEARISH"
        
        return summary
    
    def get_top_movers(self, coins: List[Dict], limit: int = 10) -> Dict:
        """
        En çok hareket eden coinleri bul
        
        Args:
            coins: Coin verileri
            limit: Gösterilecek coin sayısı
            
        Returns:
            Top gainers ve losers
        """
        sorted_coins = sorted(coins, key=lambda x: x.get("change_24h", 0), reverse=True)
        
        return {
            "top_gainers": sorted_coins[:limit],
            "top_losers": sorted_coins[-limit:]
        }
