"""
WhaleHunter WebSocket Client
wss://whalehunterapp.com'dan gerçek zamanlı whale verilerini dinler
"""
import asyncio
import json
from typing import List, Dict, Optional, Callable
from loguru import logger
import aiohttp

class WhaleHunterWSClient:
    """
    WhaleHunter WebSocket istemcisi
    """
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None, on_whale_signal: Optional[Callable] = None):
        """
        Args:
            email: WhaleHunter email (authenticated bağlantı için)
            password: WhaleHunter password
            on_whale_signal: Whale sinyali geldiğinde çağrılacak callback fonksiyonu
        """
        self.ws_url = "wss://whalehunterapp.com"
        self.email = email
        self.password = password
        self.on_whale_signal = on_whale_signal
        self.whale_data = []
        self.is_running = False
        self.cookies = None
        
    async def _get_cookies(self):
        """
        WhaleHunter'a login olup cookie'leri al
        """
        if self.cookies:
            return self.cookies
        
        if not self.email or not self.password:
            logger.warning("⚠️  Email/password yok, authenticated olmadan bağlanılacak")
            return None
        
        login_url = "https://whalehunterapp.com/login"
        
        try:
            async with aiohttp.ClientSession() as session:
                # Login
                login_data = {
                    "email": self.email,
                    "password": self.password
                }
                
                async with session.post(login_url, data=login_data, allow_redirects=True) as response:
                    if response.status == 200:
                        self.cookies = session.cookie_jar.filter_cookies(login_url)
                        logger.info("✅ WhaleHunter login başarılı")
                        return self.cookies
                    else:
                        logger.error(f"❌ Login başarısız: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"❌ Login hatası: {e}")
            return None
    
    async def connect_and_listen(self, duration_seconds: Optional[int] = None):
        """
        WebSocket'e bağlan ve whale verilerini dinle
        
        Args:
            duration_seconds: Kaç saniye dinlenecek (None = sonsuz)
        """
        logger.info(f"🔌 WhaleHunter WebSocket'e bağlanılıyor: {self.ws_url}")
        
        # Authenticated bağlantı için cookie'leri al
        await self._get_cookies()
        
        self.is_running = True
        
        try:
            # Cookie'lerle session oluştur
            async with aiohttp.ClientSession(cookies=self.cookies) as session:
                async with session.ws_connect(self.ws_url) as ws:
                    logger.info("✅ WebSocket bağlantısı kuruldu!")
                    
                    start_time = asyncio.get_event_loop().time()
                    
                    async for msg in ws:
                        if not self.is_running:
                            break
                            
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            await self._handle_message(msg.data)
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            logger.error(f"❌ WebSocket hatası: {ws.exception()}")
                            break
                        elif msg.type == aiohttp.WSMsgType.CLOSED:
                            logger.warning("⚠️  WebSocket bağlantısı kapandı")
                            break
                        
                        # Duration check
                        if duration_seconds:
                            elapsed = asyncio.get_event_loop().time() - start_time
                            if elapsed >= duration_seconds:
                                logger.info(f"⏱️  {duration_seconds} saniye doldu, bağlantı kapatılıyor")
                                break
                    
        except Exception as e:
            logger.error(f"❌ WebSocket bağlantı hatası: {e}")
        finally:
            self.is_running = False
            logger.info("🔌 WebSocket bağlantısı kapatıldı")
    
    async def _handle_message(self, raw_data: str):
        """
        WebSocket mesajını işle
        
        Args:
            raw_data: Ham JSON verisi
        """
        try:
            # Raw mesajı logla (debugging için)
            logger.debug(f"📨 WebSocket mesajı alındı: {raw_data[:200]}")
            
            data = json.loads(raw_data)
            
            # WhaleHunter'dan 2 tip mesaj gelebilir:
            # 1. type='a': Array of signals (ilk bağlantı)
            # 2. type='e': Single signal (yeni sinyal)
            
            msg_type = data.get('type')
            
            if msg_type == 'a':
                # Array of signals
                signals = data.get('message', [])
                
                if signals:
                    for signal in signals:
                        await self._process_whale_signal(signal)
                    logger.info(f"📊 {len(signals)} whale sinyali alındı")
                else:
                    logger.info("📊 Şu an aktif whale sinyali yok (boş array geldi)")
                
            elif msg_type == 'e':
                # Single signal
                signal = data.get('message')
                if signal:
                    await self._process_whale_signal(signal)
                    logger.info(f"🐋 Yeni whale sinyali: {signal.get('symbol')}")
            else:
                logger.warning(f"⚠️  Bilinmeyen mesaj tipi: {msg_type}, data: {data}")
                
        except json.JSONDecodeError:
            logger.error(f"❌ JSON parse hatası: {raw_data[:100]}")
        except Exception as e:
            logger.error(f"❌ Mesaj işleme hatası: {e}")
    
    async def _process_whale_signal(self, signal: Dict):
        """
        Whale sinyalini işle ve kaydet
        
        Args:
            signal: Whale sinyal verisi
            
        Signal format:
        {
            'symbol': 'BTCUSDT',
            'lastPrice': 28500.50,
            'percent': 12.5,  # Sinyal gücü
            'percentChange': 2.3,  # 24h değişim
            'totalUsdt': 1500000.0,  # Toplam hacim
            'signal': 1,  # 1=LONG, 0=SHORT
            'time': 1696516800000  # Timestamp
        }
        """
        # Whale verisini temizle ve formatla
        whale_entry = {
            'symbol': signal.get('symbol', ''),
            'price': signal.get('lastPrice', 0),
            'signal_strength': signal.get('percent', 0),
            'price_change_24h': signal.get('percentChange', 0),
            'volume_usdt': signal.get('totalUsdt', 0),
            'signal_type': 'LONG' if signal.get('signal') == 1 else 'SHORT',
            'timestamp': signal.get('time'),
            'strength_label': self._get_strength_label(signal.get('percent', 0))
        }
        
        # Listeye ekle
        self.whale_data.append(whale_entry)
        
        # Callback varsa çağır
        if self.on_whale_signal:
            await self.on_whale_signal(whale_entry)
    
    def _get_strength_label(self, percent: float) -> str:
        """
        Sinyal gücü etiketini belirle
        
        Args:
            percent: Sinyal yüzdesi
            
        Returns:
            'Low', 'Medium' veya 'High'
        """
        if percent < 2:
            return 'Low'
        elif percent < 10:
            return 'Medium'
        else:
            return 'High'
    
    def get_whale_data(self) -> List[Dict]:
        """
        Toplanan whale verilerini döndür
        
        Returns:
            Whale veri listesi
        """
        return self.whale_data
    
    def stop(self):
        """
        WebSocket dinlemeyi durdur
        """
        self.is_running = False
        logger.info("⏹️  WhaleHunter WebSocket dinleme durduruldu")
    
    def filter_by_symbol(self, symbols: List[str]) -> List[Dict]:
        """
        Belirli coinler için whale verilerini filtrele
        
        Args:
            symbols: Coin listesi (örn: ['BTC', 'ETH'])
            
        Returns:
            Filtrelenmiş whale verileri
        """
        # Symbol'leri normalize et (USDT ekle)
        normalized_symbols = []
        for symbol in symbols:
            if not symbol.endswith('USDT'):
                normalized_symbols.append(symbol + 'USDT')
            else:
                normalized_symbols.append(symbol)
        
        # Filtrele
        filtered = [
            entry for entry in self.whale_data 
            if entry['symbol'] in normalized_symbols
        ]
        
        return filtered
    
    def get_top_whales(self, limit: int = 10, signal_type: Optional[str] = None) -> List[Dict]:
        """
        En güçlü whale sinyallerini getir
        
        Args:
            limit: Kaç adet gösterilecek
            signal_type: 'LONG' veya 'SHORT' (None = tümü)
            
        Returns:
            Top whale listesi
        """
        data = self.whale_data
        
        # Signal type filtresi
        if signal_type:
            data = [d for d in data if d['signal_type'] == signal_type]
        
        # Sinyal gücüne göre sırala
        sorted_data = sorted(data, key=lambda x: x['signal_strength'], reverse=True)
        
        return sorted_data[:limit]
