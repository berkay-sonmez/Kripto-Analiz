"""
WhaleHunter Canlı İzleme ve Bildirim Botu
High/Medium sinyalleri tespit edip kullanıcıyı uyarır
"""
import asyncio
import json
from pathlib import Path
import sys
import os
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

from loguru import logger
from src.config.my_watchlist import MY_WATCHLIST

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import winsound  # Windows ses için
except ImportError as e:
    logger.error(f"❌ Gerekli paket kurulu değil: {e}")
    sys.exit(1)

class WhaleAlertBot:
    """
    Whale sinyallerini takip edip kullanıcıyı uyaran bot
    """
    
    def __init__(self, email: str, password: str, min_volume_usdt: float = 50000):
        self.email = email
        self.password = password
        self.base_url = "https://whalehunterapp.com"
        self.driver = None
        
        # Filtreler
        self.min_volume_usdt = min_volume_usdt  # Minimum hacim ($50k)
        
        # Sinyal takibi
        self.signal_history = defaultdict(list)  # coin -> [signals]
        self.alerted_signals = set()  # Duplicate alert önlemek için
        self.processed_rows = set()  # İşlenmiş satırları takip et
        
        # 🔥 SİNYAL YOĞUNLUĞU TESPİTİ (Aynı coinde çok sinyal = BÜYÜK HAREKET!)
        self.high_activity_threshold = 5  # 30 dakika içinde 5+ sinyal = yoğun aktivite
        self.activity_window_minutes = 30  # Son 30 dakikaya bak
        self.high_activity_alerted = {}  # coin -> son yoğunluk alert zamanı
        
        # Watchlist coinleri USDT ekleyerek hazırla
        self.watchlist_symbols = set()
        for coin in MY_WATCHLIST:
            if not coin.endswith('USDT'):
                self.watchlist_symbols.add(coin + 'USDT')
            else:
                self.watchlist_symbols.add(coin)
        
        logger.info(f"📋 Watchlist'te {len(self.watchlist_symbols)} coin takip edilecek")
        logger.info(f"💰 Minimum hacim filtresi: ${self.min_volume_usdt:,.0f}")
        logger.info(f"🔥 Yoğunluk tespiti: {self.high_activity_threshold}+ sinyal / {self.activity_window_minutes} dakika")
    
    def setup_driver(self):
        """Chrome WebDriver'ı hazırla"""
        logger.info("🌐 Chrome WebDriver başlatılıyor...")
        
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("✅ Chrome başlatıldı")
        except Exception as e:
            logger.error(f"❌ Chrome başlatma hatası: {e}")
            raise
    
    def login(self):
        """WhaleHunter'a giriş yap"""
        logger.info(f"🔐 Login: {self.email}")
        
        try:
            self.driver.get(f"{self.base_url}/login")
            import time
            time.sleep(2)
            
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(self.email)
            
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(self.password)
            
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            time.sleep(5)
            
            logger.info("✅ Login başarılı")
            return True
            
        except Exception as e:
            logger.error(f"❌ Login hatası: {e}")
            return False
    
    def go_to_futures_page(self):
        """Binance Futures sayfasına git"""
        logger.info("📊 Binance Futures sayfasına gidiliyor...")
        
        try:
            self.driver.get(f"{self.base_url}/binance-futures")
            import time
            time.sleep(5)
            
            logger.info("✅ Binance Futures sayfası yüklendi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Sayfa yükleme hatası: {e}")
            return False
    
    def play_alert_sound(self, strength: str):
        """
        Uyarı sesi çal - HIGH için ÖZEL ALARM!
        
        Args:
            strength: 'High', 'Medium', 'Low'
        """
        try:
            import time
            if 'High' in strength:
                # 🔥 HIGH: GÜÇLÜ ALARM - 5 kez yüksek sesle!
                logger.info("🔊 HIGH STRENGTH ALARM! (5x bip)")
                for i in range(5):
                    winsound.Beep(1500, 300)  # 1500Hz (daha yüksek), 300ms (daha uzun)
                    time.sleep(0.15)
                # Ekstra vurgu için 3 hızlı bip daha
                for _ in range(3):
                    winsound.Beep(2000, 150)  # Çok yüksek ton
                    time.sleep(0.05)
            elif 'Medium' in strength:
                # Medium: 2 kez normal bip
                for _ in range(2):
                    winsound.Beep(800, 200)
                    time.sleep(0.1)
            else:
                # Low: 1 kez bip
                winsound.Beep(600, 200)
        except Exception as e:
            logger.debug(f"Ses çalma hatası: {e}")
    
    def send_alert(self, whale_data: dict, reason: str):
        """
        Kullanıcıya alert gönder
        
        Args:
            whale_data: Whale sinyal verisi
            reason: Neden alert gönderildiği
        """
        symbol = whale_data['symbol']
        signal_type = whale_data['signal_type']
        strength = whale_data['strength']
        price = whale_data['last_price']
        volume = whale_data['total_usdt']
        change_24h = whale_data['change_24h']
        
        # Unique ID oluştur (duplicate önlemek için)
        time_val = whale_data.get('time', 'NOTIME')
        count_val = whale_data.get('count', 'NOCOUNT')
        alert_id = f"{symbol}_{signal_type}_{strength}_{time_val}_{count_val}"
        
        if alert_id in self.alerted_signals:
            logger.debug(f"⏩ {symbol}: Duplicate, atlanıyor")
            return  # Zaten alert gönderilmiş
        
        self.alerted_signals.add(alert_id)
        
        # Ses çal
        self.play_alert_sound(strength)
        
        # Konsol bildirimi - HIGH için ÖZEL TASARIM!
        if 'High' in strength:
            # 🔥 HIGH SİNYAL - KIRMIZI/SARI RENK!
            alert_message = f"""
\033[91m{'█'*80}\033[0m
\033[93m{'█'*80}\033[0m
\033[91m{'█'*80}\033[0m
\033[93m╔{'═'*78}╗\033[0m
\033[93m║\033[91m{'🔥'*39}\033[93m║\033[0m
\033[93m║\033[91m           ⚡⚡⚡ HIGH STRENGTH WHALE ALERT! ⚡⚡⚡              \033[93m║\033[0m
\033[93m║\033[91m{'🔥'*39}\033[93m║\033[0m
\033[93m╠{'═'*78}╣\033[0m
\033[93m║\033[0m ⏰ Zaman: \033[96m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m{' '*(80-len(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))-13)}\033[93m║\033[0m
\033[93m║\033[0m 📍 Coin: \033[92m{symbol}\033[0m{' '*(80-len(symbol)-13)}\033[93m║\033[0m
\033[93m║\033[0m 📊 Sinyal: \033[91m{signal_type} ({strength})\033[0m{' '*(80-len(signal_type)-len(strength)-15)}\033[93m║\033[0m
\033[93m║\033[0m 💵 Fiyat: {price}{' '*(80-len(str(price))-13)}\033[93m║\033[0m
\033[93m║\033[0m 📈 24h Değişim: {change_24h}{' '*(80-len(str(change_24h))-19)}\033[93m║\033[0m
\033[93m║\033[0m 💰 Hacim: \033[95m{volume} USDT\033[0m{' '*(80-len(str(volume))-18)}\033[93m║\033[0m
\033[93m║\033[0m 🎯 Sebep: \033[91m{reason}\033[0m{' '*(80-len(reason)-13)}\033[93m║\033[0m
\033[93m╠{'═'*78}╣\033[0m
\033[93m║\033[91m  🚀 HEMEN İŞLEM AÇMAYI DÜŞÜNÜN! BÜYÜK HAMLENİN TAM ZAMANI! 🚀  \033[93m║\033[0m
\033[93m╚{'═'*78}╝\033[0m
\033[91m{'█'*80}\033[0m
\033[93m{'█'*80}\033[0m
\033[91m{'█'*80}\033[0m
            """
        else:
            # MEDIUM/LOW Sinyal - Normal tasarım
            alert_message = f"""
{'='*70}
🚨 WHALE ALERT! 🚨
{'='*70}
⏰ Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Coin: {symbol}
📊 Sinyal: {signal_type} ({strength})
💵 Fiyat: {price}
📈 24h Değişim: {change_24h}
💰 Hacim: {volume} USDT
🎯 Sebep: {reason}
{'='*70}
💡 İŞLEM ÖNERİSİ: Bu coini kontrol edin ve işlem açmayı düşünün!
{'='*70}
            """
        
        logger.warning(alert_message)
        
        # Desktop bildirim (opsiyonel - Windows 10/11)
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(
                f"🐋 WHALE ALERT: {symbol}",
                f"{signal_type} - {strength}\nHacim: {volume} USDT",
                duration=10,
                threaded=True
            )
        except:
            pass  # win10toast yoksa sessizce geç
    
    def check_high_activity(self, symbol: str) -> bool:
        """
        Bir coinde son X dakikada çok fazla sinyal var mı kontrol et
        Çok sinyal = BÜYÜK HAREKET başlıyor olabilir!
        
        Args:
            symbol: Coin sembolü
            
        Returns:
            True: Yoğun aktivite var ve alert edilmeli, False: Normal
        """
        from datetime import datetime, timedelta
        
        now = datetime.now()
        history = self.signal_history[symbol]
        
        # Son X dakikadaki sinyalleri say
        window_start = now - timedelta(minutes=self.activity_window_minutes)
        recent_signals = [
            s for s in history 
            if s.get('time') and datetime.fromisoformat(s['time']) >= window_start
        ]
        
        signal_count = len(recent_signals)
        
        # Yoğun aktivite var mı?
        if signal_count >= self.high_activity_threshold:
            # Daha önce alert verdik mi? (10 dakikada bir yoğunluk alerti yeter)
            last_activity_alert = self.high_activity_alerted.get(symbol)
            if last_activity_alert:
                minutes_since = (now - last_activity_alert).total_seconds() / 60
                if minutes_since < 10:  # 10 dakika içinde tekrar etme
                    return False
            
            # 🔥 YOĞUN AKTİVİTE ALERT!
            self.high_activity_alerted[symbol] = now
            
            # LONG mu SHORT mu dominant?
            longs = sum(1 for s in recent_signals if s.get('signal_type') == 'LONG')
            shorts = sum(1 for s in recent_signals if s.get('signal_type') == 'SHORT')
            
            direction = "LONG" if longs > shorts else "SHORT" if shorts > longs else "MİXED"
            
            # ÖZEL YOĞUNLUK ALERTI
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
            
            # ÖZEL SES: 10 hızlı bip
            try:
                import time
                for _ in range(10):
                    winsound.Beep(1800, 100)  # Yüksek ton, kısa bip
                    time.sleep(0.05)
            except:
                pass
            
            return True
        
        return False
    
    def check_signal_pattern(self, symbol: str, new_signal: dict):
        """
        Coin için sinyal kontrol et ve alert kararı ver
        
        Args:
            symbol: Coin sembolü
            new_signal: Yeni gelen sinyal
            
        Returns:
            True: Alert gönderilmeli, False: Gönderilmemeli
        """
        strength = new_signal['strength']
        signal_type = new_signal['signal_type']
        
        #  ÖNCELİKLE YOĞUNLUK KONTROLÜ YAP!
        # Eğer bu coinde son 30 dakikada çok sinyal varsa özel alert ver
        self.check_high_activity(symbol)
        
        # 🎯 SİNYAL ALERTLERİ (STRENGTH BAZLI)
        
        # 1. HIGH sinyal → ANINDA alert (HACİM FİLTRESİ YOK!)
        if 'High' in strength:
            self.send_alert(new_signal, "⚡ HIGH STRENGTH SİNYAL!")
            return True
        
        # 2. MEDIUM sinyal → ANINDA ALERT! (Basit ve etkili)
        if 'Medium' in strength:
            self.send_alert(new_signal, f"📊 MEDIUM {signal_type} SİNYALİ!")
            return True
        
        # 3. LOW sinyaller → GÖRMEZDEN GEL (gereksiz)
        logger.debug(f"⏩ {symbol}: LOW sinyal atlandı (sadece HIGH/MEDIUM takip ediliyor)")
        return False
    
    def monitor_whales(self, duration_minutes: int = 60):
        """
        Whale verilerini sürekli izle - SADECE VERİ AKIŞI!
        
        Args:
            duration_minutes: Kaç dakika izlenecek (0 = sonsuz)
        """
        logger.info(f"🔍 Whale takibi başlıyor...")
        if duration_minutes == 0:
            logger.info("⏰ Süresiz izleme - Ctrl+C ile durdurun")
        else:
            logger.info(f"⏰ {duration_minutes} dakika boyunca izlenecek")
        
        logger.info("\n📋 Watchlist coinleri:")
        for coin in sorted(list(self.watchlist_symbols)[:10]):
            logger.info(f"  • {coin}")
        if len(self.watchlist_symbols) > 10:
            logger.info(f"  ... ve {len(self.watchlist_symbols) - 10} coin daha\n")
        
        logger.info("🚀 CANLI VERİ AKIŞI BAŞLADI - Her sinyal anında işlenecek!\n")
        
        import time
        from datetime import datetime, timedelta
        
        start_time = time.time()
        total_alerts = 0
        
        # Coin başına sinyal sayacı (gün içinde)
        coin_signals_today = {}  # {symbol: [{'time': dt, 'signal_type': str, 'strength': str}, ...]}
        coin_repeat_alert_sent = {}  # {symbol: datetime} - 2+ sinyal alerti gönderildi mi?
        
        try:
            while True:
                # Süre kontrolü
                if duration_minutes > 0:
                    elapsed_minutes = (time.time() - start_time) / 60
                    if elapsed_minutes >= duration_minutes:
                        logger.info(f"\n⏱️  {duration_minutes} dakika doldu, izleme sonlandırılıyor")
                        break
                
                try:
                    # DataTable'daki satırları oku
                    table = self.driver.find_element(By.ID, "example")
                    tbody = table.find_element(By.TAG_NAME, "tbody")
                    rows = tbody.find_elements(By.TAG_NAME, "tr")
                    
                    # "No data available" kontrolü
                    if len(rows) == 1:
                        first_cell = rows[0].find_element(By.TAG_NAME, "td")
                        if "No data available" in first_cell.text:
                            time.sleep(3)
                            continue
                    
                    # Her satırı kontrol et - YENİ sinyaller için
                    for row in rows:
                        logger.info(f"🔄 İlk tarama: {len(rows)} mevcut sinyal yükleniyor...")
                        logger.info(f"⚡ HIGH ve MEDIUM sinyaller için ALERT VERİLECEK!\n")
                        
                        high_count = 0
                        medium_count = 0
                        
                        for row in rows:
                            try:
                                cells = row.find_elements(By.TAG_NAME, "td")
                                if len(cells) >= 11:
                                    # Benzersiz ID oluştur (time + symbol + count)
                                    row_id = f"{cells[0].text}_{cells[2].text}_{cells[1].text}"
                                    self.processed_rows.add(row_id)
                                    
                                    # Tam whale data oluştur
                                    whale_data = {
                                        'time': cells[0].text,
                                        'count': cells[1].text,
                                        'symbol': cells[2].text,
                                        'last_price': cells[3].text,
                                        'percent': cells[4].text,
                                        'change_24h': cells[5].text,
                                        'total_usdt': cells[6].text,
                                        'signal_type': cells[7].text,
                                        'long_usdt': cells[8].text,
                                        'short_usdt': cells[9].text,
                                        'strength': cells[10].text,
                                    }
                                    
                                    # Geçmişe ekle (pattern için)
                                    self.signal_history[whale_data['symbol']].append(whale_data)
                                    
                                    # Count kaydet
                                    strength = whale_data['strength']
                                    if 'High' in strength:
                                        high_count += 1
                                    elif 'Medium' in strength:
                                        medium_count += 1
                            except:
                                continue
                        
                        # ⚡ İLK TARAMA BİTTİ - Tüm HIGH/MEDIUM için alert gönder!
                        for symbol, signals in self.signal_history.items():
                            # HIGH sinyaller - hepsini alert et
                            high_signals = [s for s in signals if 'High' in s.get('strength', '')]
                            for high_signal in high_signals:
                                self.send_alert(high_signal, "⚡ HIGH STRENGTH SİNYAL!")
                                total_alerts += 1
                            
                            # MEDIUM sinyaller - hepsini alert et
                            medium_signals = [s for s in signals if 'Medium' in s.get('strength', '')]
                            for medium_signal in medium_signals:
                                self.send_alert(medium_signal, f"📊 MEDIUM {medium_signal.get('signal_type')} SİNYALİ!")
                                total_alerts += 1
                        
                        first_scan = False
                        last_row_count = len(rows)
                        logger.info(f"✅ İlk yükleme tamamlandı!")
                        logger.info(f"📊 İlk taramada: {high_count} HIGH, {medium_count} MEDIUM sinyal bulundu")
                        logger.info(f"🚨 {total_alerts} alert gönderildi\n")
                        logger.info(f"🔄 Şimdi YENİ sinyaller bekleniyor...\n")
                        time.sleep(3)
                        continue
                    
                    # Yeni veri var mı?
                    current_row_count = len(rows)
                    if current_row_count > last_row_count:
                        new_count = current_row_count - last_row_count
                        logger.info(f"🆕 {new_count} YENİ sinyal tespit edildi!")
                        last_row_count = current_row_count
                    
                    # Her satırı kontrol et (sadece YENİ olanlar)
                    for row in rows:
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            
                            if len(cells) >= 11:
                                # Benzersiz ID oluştur
                                row_id = f"{cells[0].text}_{cells[2].text}_{cells[1].text}"
                                
                                # Zaten işlendi mi?
                                if row_id in self.processed_rows:
                                    continue  # ATLA
                                
                                # İşaretlenen sete ekle
                                self.processed_rows.add(row_id)
                                
                                # Whale data oluştur
                                whale_data = {
                                    'time': cells[0].text,
                                    'count': cells[1].text,
                                    'symbol': cells[2].text,
                                    'last_price': cells[3].text,
                                    'percent': cells[4].text,
                                    'change_24h': cells[5].text,
                                    'total_usdt': cells[6].text,
                                    'signal_type': cells[7].text,
                                    'long_usdt': cells[8].text,
                                    'short_usdt': cells[9].text,
                                    'strength': cells[10].text,
                                }
                                
                                symbol = whale_data['symbol']
                                
                                # Sinyal geçmişine ekle
                                self.signal_history[symbol].append(whale_data)
                                
                                # Son 10 sinyali tut (memory)
                                if len(self.signal_history[symbol]) > 10:
                                    self.signal_history[symbol] = self.signal_history[symbol][-10:]
                                
                                # ⚠️ YENİ SİNYAL - Sadece HIGH/2+MEDIUM için alert
                                # LOW ve tek MEDIUM sessizce atlanır
                                if self.check_signal_pattern(symbol, whale_data):
                                    total_alerts += 1
                                    logger.success(f"✅ {symbol}: Alert gönderildi! ({whale_data['strength']} {whale_data['signal_type']})")
                        
                        except Exception as e:
                            continue
                    
                    time.sleep(2)  # 2 saniye bekle
                    
                except Exception as e:
                    logger.debug(f"Tablo okuma hatası: {e}")
                    time.sleep(2)
                    continue
            
            logger.info(f"\n✅ İzleme tamamlandı. Toplam {total_alerts} alert gönderildi.")
            
        except KeyboardInterrupt:
            logger.info(f"\n⏹️  Kullanıcı tarafından durduruldu. Toplam {total_alerts} alert gönderildi.")
    
    def close(self):
        """Browser'ı kapat"""
        if self.driver:
            logger.info("🔒 Browser kapatılıyor...")
            self.driver.quit()

def main():
    email = os.getenv("WHALEHUNTER_EMAIL")
    password = os.getenv("WHALEHUNTER_PASSWORD")
    min_volume = float(os.getenv("MIN_VOLUME", "50000"))  # Varsayılan: $50k
    
    if not email or not password:
        logger.error("❌ .env dosyasında WHALEHUNTER_EMAIL ve WHALEHUNTER_PASSWORD gerekli!")
        return
    
    logger.info(f"""
╔══════════════════════════════════════════════════════════════╗
║           🐋 WHALE ALERT BOT - CANLI İZLEME 🐋             ║
╚══════════════════════════════════════════════════════════════╝

📊 Özellikler:
  • HIGH strength sinyal → ANINDA alert (8x bip - KIRMIZI/SARI)
  • MEDIUM sinyal → ANINDA alert (2x bip)
  • 30 dk içinde 5+ sinyal → 🔥 YOĞUNLUK ALERTI (10x bip)
  • Watchlist coinleri özel takip
  • Ses + renkli konsol bildirimi

⚙️  Ayarlar:
  • İzleme süresi: 24 SAAT (Sürekli)
  • Watchlist: {len(MY_WATCHLIST)} coin
  • Sadece HIGH/MEDIUM takip (LOW yok!)

🎯 SİNYAL FİLTRESİ:
  • HIGH sinyal → ✅ ANINDA alert (8x bip - kırmızı/sarı)
  • MEDIUM sinyal → ✅ ANINDA alert (2x bip)
  • LOW sinyal → ❌ Tamamen görmezden geliniyor
  
🔥 YOĞUNLUK TESPİTİ:
  • Bir coinde 30 dakikada 5+ sinyal → 🚨 BÜYÜK HAREKET UYARISI!
  • Hangi yön dominant gösterir (LONG/SHORT/MIXED)
  • 10 hızlı bip ile özel uyarı!

🎯 Kullanım:
  • Alert geldiğinde sesi duyacaksınız
  • Konsola detaylı bilgi yazılacak
  • Arka planda sürekli çalışır
  • Ctrl+C ile durdurun
    """)
    
    bot = WhaleAlertBot(email, password, min_volume_usdt=min_volume)
    
    try:
        # 1. Browser'ı başlat
        bot.setup_driver()
        
        # 2. Login
        if not bot.login():
            return
        
        # 3. Futures sayfasına git
        if not bot.go_to_futures_page():
            return
        
        # 4. Whale takibini başlat
        # 0 = Sürekli çalışma (24 saat), Test: 5, Kısa: 60
        bot.monitor_whales(duration_minutes=0)  # SONSUZ İZLEME
        
    except Exception as e:
        logger.error(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        bot.close()

if __name__ == "__main__":
    main()
