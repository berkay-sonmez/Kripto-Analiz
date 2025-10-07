"""
Binance API Client
TradingView yerine Binance API kullanır (rate limit yok!)
"""

import asyncio
from typing import List, Dict
import ccxt.async_support as ccxt
from loguru import logger
import pandas as pd
import pandas_ta as ta


class BinanceClient:
    """Binance API ile veri çekme ve teknik analiz"""
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        Binance client başlat
        
        Args:
            api_key: Binance API anahtarı (opsiyonel, public data için gerekli değil)
            api_secret: Binance API secret (opsiyonel)
        """
        self.exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,  # Otomatik rate limiting
        })
        # Spot market'i kullan
        self.exchange.options['defaultType'] = 'spot'
        logger.info("Binance client başlatıldı")
    
    async def fetch_ohlcv(self, symbol: str, timeframe: str = '15m', limit: int = 100) -> pd.DataFrame:
        """
        OHLCV (Open, High, Low, Close, Volume) verilerini çek
        
        Args:
            symbol: Coin sembolü (örn: "BTC")
            timeframe: Zaman dilimi (1m, 5m, 15m, 1h, 4h, 1d)
            limit: Çekilecek mum sayısı
            
        Returns:
            OHLCV DataFrame
        """
        try:
            # Binance formatına çevir (BTC -> BTC/USDT)
            pair = f"{symbol}/USDT"
            
            # OHLCV verilerini çek
            ohlcv = await self.exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
            
            # DataFrame'e çevir
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.warning(f"❌ {symbol} OHLCV verisi çekilemedi: {e}")
            return pd.DataFrame()
    
    async def calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """
        Teknik indikatörleri hesapla
        
        Args:
            df: OHLCV DataFrame
            
        Returns:
            İndikatörler dictionary
        """
        if df.empty:
            return {}
        
        try:
            # RSI
            df['rsi'] = ta.rsi(df['close'], length=14)
            
            # MACD
            macd = ta.macd(df['close'])
            df['macd'] = macd['MACD_12_26_9']
            df['macd_signal'] = macd['MACDs_12_26_9']
            df['macd_hist'] = macd['MACDh_12_26_9']
            
            # Bollinger Bands
            bbands = ta.bbands(df['close'], length=20)
            df['bb_upper'] = bbands['BBU_20_2.0']
            df['bb_middle'] = bbands['BBM_20_2.0']
            df['bb_lower'] = bbands['BBL_20_2.0']
            
            # EMA (Exponential Moving Average)
            df['ema_9'] = ta.ema(df['close'], length=9)
            df['ema_21'] = ta.ema(df['close'], length=21)
            df['ema_50'] = ta.ema(df['close'], length=50)
            
            # SMA (Simple Moving Average)
            df['sma_20'] = ta.sma(df['close'], length=20)
            df['sma_50'] = ta.sma(df['close'], length=50)
            df['sma_200'] = ta.sma(df['close'], length=200)
            
            # Stochastic
            stoch = ta.stoch(df['high'], df['low'], df['close'])
            df['stoch_k'] = stoch['STOCHk_14_3_3']
            df['stoch_d'] = stoch['STOCHd_14_3_3']
            
            # ATR (Average True Range)
            df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=14)
            
            # Volume indicators
            df['volume_sma'] = ta.sma(df['volume'], length=20)
            
            # En son değerleri al
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            
            # 24h değişim hesapla
            price_change = ((last['close'] - df.iloc[0]['close']) / df.iloc[0]['close']) * 100
            
            return {
                # Fiyat bilgileri
                'price': float(last['close']),
                'open': float(last['open']),
                'high': float(last['high']),
                'low': float(last['low']),
                'volume': float(last['volume']),
                'change_24h': float(price_change),
                
                # RSI
                'rsi': float(last['rsi']) if not pd.isna(last['rsi']) else 50.0,
                
                # MACD
                'macd': float(last['macd']) if not pd.isna(last['macd']) else 0.0,
                'macd_signal': float(last['macd_signal']) if not pd.isna(last['macd_signal']) else 0.0,
                'macd_hist': float(last['macd_hist']) if not pd.isna(last['macd_hist']) else 0.0,
                
                # Bollinger Bands
                'bb_upper': float(last['bb_upper']) if not pd.isna(last['bb_upper']) else 0.0,
                'bb_middle': float(last['bb_middle']) if not pd.isna(last['bb_middle']) else 0.0,
                'bb_lower': float(last['bb_lower']) if not pd.isna(last['bb_lower']) else 0.0,
                
                # Moving Averages
                'ema_9': float(last['ema_9']) if not pd.isna(last['ema_9']) else 0.0,
                'ema_21': float(last['ema_21']) if not pd.isna(last['ema_21']) else 0.0,
                'ema_50': float(last['ema_50']) if not pd.isna(last['ema_50']) else 0.0,
                'sma_20': float(last['sma_20']) if not pd.isna(last['sma_20']) else 0.0,
                'sma_50': float(last['sma_50']) if not pd.isna(last['sma_50']) else 0.0,
                'sma_200': float(last['sma_200']) if not pd.isna(last['sma_200']) else 0.0,
                
                # Stochastic
                'stoch_k': float(last['stoch_k']) if not pd.isna(last['stoch_k']) else 50.0,
                'stoch_d': float(last['stoch_d']) if not pd.isna(last['stoch_d']) else 50.0,
                
                # ATR
                'atr': float(last['atr']) if not pd.isna(last['atr']) else 0.0,
                
                # Volume
                'volume_sma': float(last['volume_sma']) if not pd.isna(last['volume_sma']) else 0.0,
                
                # Raw DataFrame (isteğe bağlı detaylı analiz için)
                'dataframe': df
            }
            
        except Exception as e:
            logger.error(f"İndikatör hesaplama hatası: {e}")
            return {}
    
    async def fetch_coin_data(self, symbol: str, timeframe: str = '15m') -> Dict:
        """
        Tek bir coin için detaylı veri ve indikatörleri çek
        
        Args:
            symbol: Coin sembolü
            timeframe: Zaman dilimi
            
        Returns:
            Coin verisi ve tüm indikatörler
        """
        try:
            # OHLCV verilerini çek
            df = await self.fetch_ohlcv(symbol, timeframe=timeframe, limit=200)
            
            if df.empty:
                return None
            
            # İndikatörleri hesapla
            indicators = await self.calculate_indicators(df)
            
            if not indicators:
                return None
            
            # Temel sinyal üretimi
            rsi = indicators['rsi']
            macd_hist = indicators['macd_hist']
            price = indicators['price']
            ema_9 = indicators['ema_9']
            ema_21 = indicators['ema_21']
            
            # Basit öneri mantığı
            buy_signals = 0
            sell_signals = 0
            
            # RSI sinyalleri
            if rsi < 30:
                buy_signals += 2
            elif rsi > 70:
                sell_signals += 2
            elif rsi < 40:
                buy_signals += 1
            elif rsi > 60:
                sell_signals += 1
            
            # MACD sinyalleri
            if macd_hist > 0:
                buy_signals += 1
            else:
                sell_signals += 1
            
            # EMA cross sinyalleri
            if ema_9 > ema_21:
                buy_signals += 1
            else:
                sell_signals += 1
            
            # Öneri belirle
            if buy_signals > sell_signals + 2:
                recommendation = "STRONG_BUY"
            elif buy_signals > sell_signals:
                recommendation = "BUY"
            elif sell_signals > buy_signals + 2:
                recommendation = "STRONG_SELL"
            elif sell_signals > buy_signals:
                recommendation = "SELL"
            else:
                recommendation = "NEUTRAL"
            
            return {
                'symbol': symbol,
                'exchange': 'BINANCE',
                'timeframe': timeframe,
                'recommendation': recommendation,
                'buy_signals': buy_signals,
                'sell_signals': sell_signals,
                **indicators
            }
            
        except Exception as e:
            logger.warning(f"❌ {symbol} verisi çekilemedi: {e}")
            return None
    
    async def fetch_multiple_coins(self, symbols: List[str], timeframe: str = '15m') -> List[Dict]:
        """
        Birden fazla coin için paralel veri çekme
        
        Args:
            symbols: Coin sembolleri listesi
            timeframe: Zaman dilimi
            
        Returns:
            Coin verileri listesi
        """
        logger.info(f"📥 {len(symbols)} coin için veri çekiliyor... (Binance API)")
        
        # Paralel çekme
        tasks = [self.fetch_coin_data(symbol, timeframe) for symbol in symbols]
        results = await asyncio.gather(*tasks)
        
        # Başarılı sonuçları filtrele
        coins = [r for r in results if r is not None]
        
        logger.info(f"✅ {len(coins)}/{len(symbols)} coin verisi başarıyla çekildi")
        return coins
    
    async def close(self):
        """Exchange bağlantısını kapat"""
        await self.exchange.close()
