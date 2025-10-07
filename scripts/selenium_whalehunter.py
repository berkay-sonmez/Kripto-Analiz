"""
WhaleHunter Selenium Scraper
Browser'ı otomatik açıp whale verilerini çeker
"""
import asyncio
import json
import time
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# .env dosyasını yükle
load_dotenv()

from loguru import logger

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    logger.error("❌ Selenium kurulu değil! Yüklemek için: pip install selenium webdriver-manager")
    sys.exit(1)

class WhaleHunterSeleniumScraper:
    """
    Selenium ile WhaleHunter'dan veri çek
    """
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        self.base_url = "https://whalehunterapp.com"
        self.driver = None
        
    def setup_driver(self):
        """
        Chrome WebDriver'ı hazırla (otomatik ChromeDriver indirme)
        """
        logger.info("🌐 Chrome WebDriver başlatılıyor...")
        
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Görünmez mod (test için kapalı, görmek için yorum satırı)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bot tespitini engelle
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # WebDriver'ı başlat (otomatik ChromeDriver yönetimi)
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Chrome başlatıldı")
        except Exception as e:
            logger.error(f"❌ Chrome başlatma hatası: {e}")
            logger.info("💡 Chrome browser kurulu mu? Yüklemek için: https://www.google.com/chrome/")
            raise
    
    def login(self):
        """
        WhaleHunter'a giriş yap
        """
        logger.info(f"🔐 Login: {self.email}")
        
        try:
            # Login sayfasına git
            self.driver.get(f"{self.base_url}/login")
            time.sleep(2)
            
            # Email input
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(self.email)
            
            # Password input
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            
            # Login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Yönlenmeyi bekle
            time.sleep(5)
            
            # Başarılı mı kontrol et
            current_url = self.driver.current_url
            logger.info(f"📍 Yönlendirilen URL: {current_url}")
            
            # Fees sayfasına gittiyse, üyelik gerekiyor demektir
            if "/fees" in current_url:
                logger.warning("⚠️  /fees sayfasına yönlendirildi - WhaleHunter PRO üyeliği gerekli olabilir")
                logger.info("💡 Ama yine de binance-futures sayfasını kontrol edelim...")
                return True  # Devam et, belki veri görebiliriz
            
            if "/binance-futures" in current_url or "/dashboard" in current_url or "/login" not in current_url:
                logger.info("✅ Login başarılı!")
                return True
            else:
                logger.error(f"❌ Login başarısız. URL: {current_url}")
                # Screenshot al
                screenshot_path = Path(project_root) / "data" / "login_error.png"
                self.driver.save_screenshot(str(screenshot_path))
                logger.info(f"📸 Screenshot kaydedildi: {screenshot_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Login hatası: {e}")
            return False
    
    def go_to_futures_page(self):
        """
        Binance Futures sayfasına git
        """
        logger.info("📊 Binance Futures sayfasına gidiliyor...")
        
        try:
            self.driver.get(f"{self.base_url}/binance-futures")
            time.sleep(5)  # Sayfanın yüklenmesini bekle
            
            logger.info("✅ Binance Futures sayfası yüklendi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Sayfa yükleme hatası: {e}")
            return False
    
    def wait_for_data(self, duration_seconds: int = 30):
        """
        Whale verilerinin gelmesini bekle
        
        Args:
            duration_seconds: Kaç saniye beklenecek
        """
        logger.info(f"⏱️  {duration_seconds} saniye boyunca whale verileri bekleniyor...")
        logger.info("💡 DataTable'da veri görünmeye başladığında otomatik olarak çekilecek\n")
        
        whale_data = []
        start_time = time.time()
        last_row_count = 0
        
        try:
            while time.time() - start_time < duration_seconds:
                try:
                    # DataTable'daki satırları bul
                    table = self.driver.find_element(By.ID, "example")
                    tbody = table.find_element(By.TAG_NAME, "tbody")
                    rows = tbody.find_elements(By.TAG_NAME, "tr")
                    
                    # "No data available" kontrolü
                    if len(rows) == 1:
                        first_cell = rows[0].find_element(By.TAG_NAME, "td")
                        if "No data available" in first_cell.text:
                            logger.debug(f"⏳ Henüz veri yok... ({int(time.time() - start_time)}s)")
                            time.sleep(2)
                            continue
                    
                    # Yeni veri var mı?
                    current_row_count = len(rows)
                    if current_row_count > last_row_count:
                        logger.info(f"📊 {current_row_count - last_row_count} yeni whale sinyali tespit edildi!")
                        last_row_count = current_row_count
                    
                    # Her satırı parse et
                    for row in rows:
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            
                            if len(cells) >= 11:  # En az 11 sütun olmalı
                                whale_entry = {
                                    'time': cells[0].text,
                                    'count': cells[1].text,
                                    'symbol': cells[2].text,
                                    'last_price': cells[3].text,
                                    'percent': cells[4].text,
                                    'change_24h': cells[5].text,
                                    'total_usdt': cells[6].text,
                                    'signal_type': cells[7].text,  # LONG/SHORT
                                    'long_usdt': cells[8].text,
                                    'short_usdt': cells[9].text,
                                    'strength': cells[10].text,  # Low/Medium/High
                                }
                                
                                # Duplicate kontrolü
                                if whale_entry not in whale_data:
                                    whale_data.append(whale_entry)
                                    
                                    # Konsola yazdır
                                    logger.info(f"""
🐋 YENİ WHALE SİNYALİ:
   Symbol: {whale_entry['symbol']}
   Type: {whale_entry['signal_type']}
   Price: {whale_entry['last_price']}
   Strength: {whale_entry['strength']}
   Volume: {whale_entry['total_usdt']}
   24h: {whale_entry['change_24h']}
                                    """)
                        
                        except Exception as e:
                            logger.debug(f"Satır parse hatası: {e}")
                            continue
                    
                    time.sleep(2)  # 2 saniye bekle
                    
                except Exception as e:
                    logger.debug(f"Tablo okuma hatası: {e}")
                    time.sleep(2)
                    continue
            
            logger.info(f"\n✅ Toplam {len(whale_data)} whale sinyali toplandı")
            return whale_data
            
        except KeyboardInterrupt:
            logger.info("\n⏹️  Kullanıcı tarafından durduruldu")
            return whale_data
    
    def capture_network_traffic(self):
        """
        Browser'ın network trafiğini yakala (WebSocket, XHR)
        """
        logger.info("🔍 Network trafiği yakalanıyor...")
        
        # Chrome DevTools Protocol kullan
        logs = self.driver.get_log('performance')
        
        websocket_urls = []
        api_endpoints = []
        
        for entry in logs:
            log = json.loads(entry['message'])['message']
            
            if 'Network.webSocketCreated' in log.get('method', ''):
                ws_url = log['params']['url']
                websocket_urls.append(ws_url)
                logger.info(f"🔌 WebSocket bulundu: {ws_url}")
            
            elif 'Network.requestWillBeSent' in log.get('method', ''):
                url = log['params']['request']['url']
                if 'api' in url or 'data' in url or 'signal' in url:
                    if url not in api_endpoints:
                        api_endpoints.append(url)
                        logger.info(f"📡 API endpoint: {url}")
        
        return {
            'websockets': websocket_urls,
            'api_endpoints': api_endpoints
        }
    
    def close(self):
        """
        Browser'ı kapat
        """
        if self.driver:
            logger.info("🔒 Browser kapatılıyor...")
            self.driver.quit()

def main():
    email = os.getenv("WHALEHUNTER_EMAIL")
    password = os.getenv("WHALEHUNTER_PASSWORD")
    
    if not email or not password:
        logger.error("❌ .env dosyasında WHALEHUNTER_EMAIL ve WHALEHUNTER_PASSWORD gerekli!")
        return
    
    scraper = WhaleHunterSeleniumScraper(email, password)
    
    try:
        # 1. Browser'ı başlat
        scraper.setup_driver()
        
        # 2. Login
        if not scraper.login():
            return
        
        # 3. Futures sayfasına git
        if not scraper.go_to_futures_page():
            return
        
        # 4. Network trafiğini yakala (opsiyonel)
        # network_info = scraper.capture_network_traffic()
        
        # 5. Whale verilerini bekle (30 saniye)
        whale_data = scraper.wait_for_data(duration_seconds=60)
        
        # 6. Verileri kaydet
        if whale_data:
            output_dir = Path(project_root) / "data"
            output_dir.mkdir(exist_ok=True)
            
            output_file = output_dir / "whalehunter_selenium_data.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(whale_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"\n💾 Veriler kaydedildi: {output_file}")
            
            # İstatistikler
            logger.info("\n📊 İSTATİSTİKLER:")
            logger.info(f"Toplam sinyal: {len(whale_data)}")
            
            # Signal type dağılımı
            long_count = sum(1 for w in whale_data if 'LONG' in w.get('signal_type', '').upper())
            short_count = sum(1 for w in whale_data if 'SHORT' in w.get('signal_type', '').upper())
            
            logger.info(f"LONG:  {long_count}")
            logger.info(f"SHORT: {short_count}")
        else:
            logger.warning("⚠️  Hiç whale verisi alınamadı")
            logger.info("💡 Muhtemelen şu an piyasada büyük hareket yok")
        
    except Exception as e:
        logger.error(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
