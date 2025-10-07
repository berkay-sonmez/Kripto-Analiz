"""
WhaleHunter API Client
whalehunterapp.com'dan whale hareketleri ve hacim verilerini çeker
"""

import asyncio
import aiohttp
from typing import List, Dict
from loguru import logger
import json


class WhaleHunterClient:
    """WhaleHunter API/Web client"""
    
    def __init__(self, email: str = None, password: str = None):
        """
        WhaleHunter client başlat
        
        Args:
            email: WhaleHunter email
            password: WhaleHunter şifre
        """
        self.base_url = "https://whalehunterapp.com"
        self.api_url = f"{self.base_url}/api"
        self.email = email
        self.password = password
        self.session = None
        self.auth_token = None
        logger.info("WhaleHunter client başlatıldı")
    
    async def login(self):
        """WhaleHunter'a giriş yap"""
        if not self.email or not self.password:
            logger.warning("WhaleHunter giriş bilgileri eksik")
            return False
        
        try:
            async with aiohttp.ClientSession() as session:
                # Login endpoint'ini dene
                login_url = f"{self.base_url}/api/login"
                
                payload = {
                    "email": self.email,
                    "password": self.password
                }
                
                async with session.post(login_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.auth_token = data.get('token') or data.get('access_token')
                        logger.info("✅ WhaleHunter giriş başarılı")
                        return True
                    else:
                        logger.error(f"❌ WhaleHunter giriş başarısız: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"WhaleHunter login hatası: {e}")
            return False
    
    async def fetch_whale_movements(self, symbol: str = None) -> List[Dict]:
        """
        Whale hareketlerini çek
        
        Args:
            symbol: Coin sembolü (opsiyonel, tümü için None)
            
        Returns:
            Whale hareketleri listesi
        """
        try:
            headers = {}
            if self.auth_token:
                headers['Authorization'] = f'Bearer {self.auth_token}'
            
            async with aiohttp.ClientSession(headers=headers) as session:
                # Whale movements endpoint
                url = f"{self.api_url}/whale-movements"
                if symbol:
                    url += f"?symbol={symbol}"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.warning(f"Whale movements çekilemedi: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Whale movements hatası: {e}")
            return []
    
    async def fetch_volume_data(self, symbols: List[str]) -> List[Dict]:
        """
        Hacim verilerini çek
        
        Args:
            symbols: Coin sembolleri
            
        Returns:
            Hacim verileri
        """
        try:
            headers = {}
            if self.auth_token:
                headers['Authorization'] = f'Bearer {self.auth_token}'
            
            async with aiohttp.ClientSession(headers=headers) as session:
                url = f"{self.api_url}/volumes"
                
                payload = {"symbols": symbols}
                
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.warning(f"Volume data çekilemedi: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Volume data hatası: {e}")
            return []
    
    async def get_signals(self) -> List[Dict]:
        """
        Real-time sinyalleri çek
        
        Returns:
            Sinyal listesi
        """
        try:
            headers = {}
            if self.auth_token:
                headers['Authorization'] = f'Bearer {self.auth_token}'
            
            async with aiohttp.ClientSession(headers=headers) as session:
                url = f"{self.api_url}/signals"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.warning(f"Signals çekilemedi: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Signals hatası: {e}")
            return []


# Web Scraping alternatifi (API yoksa)
class WhaleHunterScraper:
    """WhaleHunter web scraper (API yoksa kullan)"""
    
    def __init__(self, email: str, password: str):
        """
        Scraper başlat
        
        Args:
            email: WhaleHunter email
            password: WhaleHunter şifre
        """
        self.email = email
        self.password = password
        self.base_url = "https://whalehunterapp.com"
        self.session = None
        logger.info("WhaleHunter scraper başlatıldı")
    
    async def login_and_get_cookies(self):
        """
        Login olup cookie'leri al
        
        Returns:
            Session cookies
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Login sayfasına git
                login_url = f"{self.base_url}/login"
                
                payload = {
                    "email": self.email,
                    "password": self.password
                }
                
                async with session.post(login_url, data=payload, allow_redirects=True) as response:
                    if response.status == 200:
                        cookies = session.cookie_jar.filter_cookies(self.base_url)
                        logger.info("✅ WhaleHunter login başarılı (scraper)")
                        return cookies
                    else:
                        logger.error(f"❌ WhaleHunter login başarısız: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Login hatası: {e}")
            return None
    
    async def scrape_whale_data(self):
        """
        Whale verilerini scrape et - farklı endpoint'leri dene
        
        Returns:
            Scrape edilen veriler
        """
        cookies = await self.login_and_get_cookies()
        
        if not cookies:
            return None
        
        # Denenmesi gereken URL'ler
        urls_to_try = [
            f"{self.base_url}/binance-futures",
            f"{self.base_url}/dashboard",
            f"{self.base_url}/home",
            f"{self.base_url}/signals",
            f"{self.base_url}/whale-movements",
        ]
        
        results = {}
        
        try:
            async with aiohttp.ClientSession(cookies=cookies) as session:
                for url in urls_to_try:
                    try:
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                            if response.status == 200:
                                content_type = response.headers.get('Content-Type', '')
                                
                                if 'application/json' in content_type:
                                    # JSON data
                                    data = await response.json()
                                    results[url] = {'type': 'json', 'data': data}
                                    logger.info(f"✅ JSON data bulundu: {url}")
                                else:
                                    # HTML data
                                    html = await response.text()
                                    results[url] = {'type': 'html', 'data': html, 'length': len(html)}
                                    logger.info(f"✅ HTML data bulundu: {url} ({len(html)} bytes)")
                            else:
                                logger.debug(f"⚠️  {url}: {response.status}")
                    except Exception as e:
                        logger.debug(f"❌ {url}: {e}")
                        continue
                
                return results if results else None
                        
        except Exception as e:
            logger.error(f"Scraping hatası: {e}")
            return None
    
    async def find_api_endpoints(self):
        """
        WhaleHunter'ın API endpoint'lerini bul
        
        Returns:
            Bulunan endpoint'ler
        """
        cookies = await self.login_and_get_cookies()
        
        if not cookies:
            return None
        
        # Olası API endpoint'leri
        api_endpoints = [
            "/api/whale-movements",
            "/api/signals",
            "/api/volumes",
            "/api/futures/data",
            "/api/binance/futures",
            "/api/dashboard/data",
            "/api/live-data",
            "/api/get-signals",
            "/api/get-whales",
        ]
        
        found_endpoints = []
        
        try:
            async with aiohttp.ClientSession(cookies=cookies) as session:
                for endpoint in api_endpoints:
                    url = f"{self.base_url}{endpoint}"
                    try:
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status in [200, 201]:
                                content_type = response.headers.get('Content-Type', '')
                                if 'json' in content_type:
                                    data = await response.json()
                                    found_endpoints.append({
                                        'url': url,
                                        'status': response.status,
                                        'data_sample': str(data)[:200]
                                    })
                                    logger.info(f"✅ API bulundu: {url}")
                    except:
                        continue
                
                return found_endpoints
                        
        except Exception as e:
            logger.error(f"API arama hatası: {e}")
            return None
