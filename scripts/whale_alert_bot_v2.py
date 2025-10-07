#!/usr/bin/env python3
"""
🐋 WHALE ALERT BOT V2 - TEMİZ VE BASIT!
- Sürekli veri akışı (her 2 saniye)
- HIGH/MEDIUM → anında alert
- Aynı coinde 2+ sinyal (1 saat içinde) → özel uyarı
- "Yükleme tamamlandı" mesajı YOK - sadece akış!
"""

import os
import sys
import time
import platform
import requests
import threading
from datetime import datetime, timedelta
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from dotenv import load_dotenv

# winsound sadece Windows'ta var - Linux/Mac için alternatif
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# Load environment
load_dotenv()

# Logging config
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)


class WhaleAlertBot:
    def __init__(self):
        self.driver = None
        self.processed_rows = set()  # İşlenmiş row ID'ler
        self.signal_history = defaultdict(list)  # {symbol: [whale_data, ...]}
        self.alerted_signals = set()  # Gönderilmiş alert ID'ler
        
        # Coin bazlı sinyal takibi (gün içinde)
        self.coin_signals_today = {}  # {symbol: [{'time': dt, 'signal_type': str, 'strength': str}, ...]}
        self.coin_repeat_alert_sent = {}  # {symbol: datetime}
        
        # Telegram ayarları
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.telegram_enabled = bool(self.telegram_token and self.telegram_chat_id)
        
        logger.info(f"🎯 HIGH → 8 bip (kırmızı/sarı) | MEDIUM → 2 bip (beyaz)")
        logger.info(f"🔥 Aynı coinde 2+ sinyal (1 saat içinde) → ÖZEL UYARI!")
        logger.info(f"📊 TÜM COINLER İZLENİYOR - Filtre yok!")
        
        if self.telegram_enabled:
            logger.info(f"📱 TELEGRAM BİLDİRİMLERİ AKTİF!")
        else:
            logger.warning(f"⚠️  Telegram bildirimleri kapalı (.env dosyasında token/chat_id eksik)")
    
    def setup_driver(self):
        """Chrome WebDriver'ı başlat (Sunucu uyumlu)"""
        logger.info("🌐 Chrome WebDriver başlatılıyor...")
        
        options = Options()
        
        # Sunucu ortamı tespiti
        is_server = os.getenv("RENDER") or os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("FLY_APP_NAME")
        
        if is_server:
            logger.info("🌐 Sunucu ortamı tespit edildi - Headless mode aktif")
            options.add_argument("--headless=new")  # Yeni headless mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        else:
            logger.info("💻 Lokal ortam - Normal mode")
            options.add_argument("--start-maximized")
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        logger.info("✅ Chrome başlatıldı")
    
    def login(self):
        """WhaleHunter'a login ol"""
        email = os.getenv("WHALEHUNTER_EMAIL", "berkaysnmz1903@gmail.com")
        password = os.getenv("WHALEHUNTER_PASSWORD", "1327pc1327")
        
        logger.info(f"🔐 Login: {email}")
        
        self.driver.get("https://whalehunterapp.com/login")
        time.sleep(3)
        
        email_input = self.driver.find_element(By.NAME, "email")
        password_input = self.driver.find_element(By.NAME, "password")
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(5)
        logger.info("✅ Login başarılı")
    
    def go_to_futures_page(self):
        """WhaleHunter sayfasına git"""
        logger.info("📊 WhaleHunter futures sayfası yükleniyor...")
        
        # DOĞRU URL (eski selenium_whalehunter.py'den)
        self.driver.get("https://whalehunterapp.com/binance-futures")
        logger.info("⏳ Sayfa yükleniyor (60 saniye beklenecek)...")
        time.sleep(10)
        
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, "example"))
            )
            logger.info("✅ WhaleHunter sayfası hazır - Veri akışı başlıyor!")
        except Exception as e:
            logger.warning(f"⚠️ Tablo bulunamadı, yine de devam ediliyor: {e}")
            time.sleep(10)  # Ekstra bekle
    
    def send_telegram_message(self, message):
        """Telegram'a mesaj gönder"""
        if not self.telegram_enabled:
            return
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, data=data, timeout=5)
            if response.status_code == 200:
                logger.debug(f"📱 Telegram mesajı gönderildi")
            else:
                logger.warning(f"⚠️ Telegram hatası: {response.status_code}")
        except Exception as e:
            logger.debug(f"Telegram gönderme hatası: {e}")
    
    def play_alert_sound(self, strength):
        """Alert sesi çal (sadece Windows'ta)"""
        if not HAS_WINSOUND:
            return  # Linux/Mac'te ses yok, sadece log
        
        try:
            if 'High' in strength:
                # HIGH: 8 bip (5 uzun + 3 kısa)
                for _ in range(5):
                    winsound.Beep(1500, 300)
                    time.sleep(0.05)
                for _ in range(3):
                    winsound.Beep(2000, 150)
                    time.sleep(0.05)
            elif 'Medium' in strength:
                # MEDIUM: 2 bip
                for _ in range(2):
                    winsound.Beep(800, 200)
                    time.sleep(0.1)
        except Exception as e:
            logger.debug(f"Ses hatası: {e}")
    
    def send_alert(self, whale_data, reason):
        """Alert gönder"""
        symbol = whale_data['symbol']
        signal_type = whale_data['signal_type']
        strength = whale_data['strength']
        time_val = whale_data['time']
        count_val = whale_data['count']
        
        # Benzersiz alert ID
        alert_id = f"{symbol}_{signal_type}_{strength}_{time_val}_{count_val}"
        
        # Duplicate kontrolü
        if alert_id in self.alerted_signals:
            return
        
        self.alerted_signals.add(alert_id)
        
        # Ses çal
        self.play_alert_sound(strength)
        
        # Renkli display
        if 'High' in strength:
            # RED/YELLOW border için ANSI codes
            logger.warning(f"""
\033[91m======================================================================\033[0m
\033[93m🔥🔥🔥 HIGH STRENGTH WHALE ALERT! 🔥🔥🔥\033[0m
\033[91m======================================================================\033[0m
⏰ Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Coin: \033[93m{symbol}\033[0m
📊 Sinyal: \033[91m{signal_type}\033[0m (\033[93m{strength}\033[0m)
💵 Fiyat: {whale_data['last_price']}
📈 24h Değişim: {whale_data['change_24h']}%
💰 Hacim: {whale_data['total_usdt']} USDT
🎯 Sebep: {reason}
\033[91m======================================================================\033[0m
💡 İŞLEM ÖNERİSİ: HEMEN KONTROL EDİN - GÜÇLÜ SİNYAL!
\033[91m======================================================================\033[0m
""")
            # Telegram HIGH mesajı
            telegram_msg = f"""
🔥🔥🔥 <b>HIGH STRENGTH WHALE!</b> 🔥🔥🔥

📍 Coin: <b>{symbol}</b>
📊 Sinyal: <b>{signal_type}</b> ({strength})
💵 Fiyat: {whale_data['last_price']}
📈 24h: {whale_data['change_24h']}%
💰 Hacim: {whale_data['total_usdt']} USDT

💡 HEMEN KONTROL EDİN!
"""
            self.send_telegram_message(telegram_msg)
            
        else:
            # MEDIUM - normal white
            logger.warning(f"""
======================================================================
🚨 WHALE ALERT! 🚨
======================================================================
⏰ Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📍 Coin: {symbol}
📊 Sinyal: {signal_type} ({strength})
💵 Fiyat: {whale_data['last_price']}
📈 24h Değişim: {whale_data['change_24h']}%
💰 Hacim: {whale_data['total_usdt']} USDT
🎯 Sebep: {reason}
======================================================================
💡 İŞLEM ÖNERİSİ: Bu coini kontrol edin ve işlem açmayı düşünün!
======================================================================
""")
            # Telegram MEDIUM mesajı
            telegram_msg = f"""
🚨 <b>WHALE ALERT</b>

📍 Coin: <b>{symbol}</b>
📊 Sinyal: {signal_type} ({strength})
💵 Fiyat: {whale_data['last_price']}
📈 24h: {whale_data['change_24h']}%
💰 Hacim: {whale_data['total_usdt']} USDT
"""
            self.send_telegram_message(telegram_msg)
    
    def send_repeat_signal_alert(self, symbol, recent_signals, latest_data):
        """Tekrar sinyal uyarısı gönder (2+ sinyal aynı coinde)"""
        # 10 hızlı bip (sadece Windows)
        if HAS_WINSOUND:
            try:
                for _ in range(10):
                    winsound.Beep(1800, 100)
                    time.sleep(0.05)
            except:
                pass
        
        # Yön analizi
        long_count = sum(1 for s in recent_signals if 'Long' in s['signal_type'])
        short_count = sum(1 for s in recent_signals if 'Short' in s['signal_type'])
        
        if long_count > short_count:
            direction = f"\033[92m📈 LONG DOMINANT ({long_count}L / {short_count}S)\033[0m"
        elif short_count > long_count:
            direction = f"\033[91m📉 SHORT DOMINANT ({short_count}S / {long_count}L)\033[0m"
        else:
            direction = f"\033[95m🔄 MIXED ({long_count}L / {short_count}S)\033[0m"
        
        logger.warning(f"""
\033[96m======================================================================\033[0m
\033[93m🔥 TEKRAR SİNYAL TESPİTİ! 🔥\033[0m
\033[96m======================================================================\033[0m
📍 Coin: \033[96m{symbol}\033[0m
🔢 Son 1 saat: \033[93m{len(recent_signals)} SİNYAL!\033[0m
🎯 Yön: {direction}
💵 Son Fiyat: {latest_data['last_price']}
💰 Son Hacim: {latest_data['total_usdt']} USDT
\033[96m======================================================================\033[0m
💡 Bu coinde YOĞUN AKTİVİTE var - ÖNCELİK VERİN!
\033[96m======================================================================\033[0m
""")
        
        # Telegram TEKRAR SİNYAL mesajı
        if long_count > short_count:
            tg_direction = f"📈 LONG DOMINANT ({long_count}L / {short_count}S)"
        elif short_count > long_count:
            tg_direction = f"📉 SHORT DOMINANT ({short_count}S / {long_count}L)"
        else:
            tg_direction = f"🔄 MIXED ({long_count}L / {short_count}S)"
        
        telegram_msg = f"""
🔥🔥 <b>TEKRAR SİNYAL!</b> 🔥🔥

📍 Coin: <b>{symbol}</b>
🔢 Son 1 saat: <b>{len(recent_signals)} SİNYAL!</b>
🎯 Yön: {tg_direction}
💵 Son Fiyat: {latest_data['last_price']}
💰 Son Hacim: {latest_data['total_usdt']} USDT

💡 YOĞUN AKTİVİTE - ÖNCELİK VERİN!
"""
        self.send_telegram_message(telegram_msg)
    
    def monitor_whales(self, duration_minutes=0):
        """Whale verilerini sürekli izle - SADECE VERİ AKIŞI!"""
        logger.info(f"🔍 WhaleHunter veri akışı başlıyor...")
        if duration_minutes == 0:
            logger.info("⏰ Süresiz izleme - Ctrl+C ile durdurun")
        else:
            logger.info(f"⏰ {duration_minutes} dakika boyunca izlenecek")
        
        logger.info("🚀 CANLI VERİ AKIŞI BAŞLADI - Her sinyal anında işlenecek!\n")
        
        start_time = time.time()
        total_alerts = 0
        last_refresh_time = time.time()  # Sayfa yenileme takibi
        refresh_interval = 60  # 60 saniyede bir sayfa yenile
        
        try:
            while True:
                # Süre kontrolü
                if duration_minutes > 0:
                    elapsed_minutes = (time.time() - start_time) / 60
                    if elapsed_minutes >= duration_minutes:
                        logger.info(f"\n⏱️  {duration_minutes} dakika doldu, izleme sonlandırılıyor")
                        break
                
                # Sayfa yenileme kontrolü - GÜNCEL VERİ ÇEK!
                current_time = time.time()
                if current_time - last_refresh_time >= refresh_interval:
                    logger.info("🔄 Sayfa yenileniyor - Güncel veriler çekiliyor...")
                    self.driver.refresh()
                    time.sleep(3)  # Sayfa yüklensin
                    last_refresh_time = current_time
                    logger.info("✅ Sayfa yenilendi - Veri akışı devam ediyor")
                
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
                        try:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            
                            if len(cells) >= 11:
                                # Benzersiz ID oluştur
                                row_id = f"{cells[0].text}_{cells[2].text}_{cells[1].text}"
                                
                                # Zaten işlendi mi?
                                if row_id in self.processed_rows:
                                    continue  # ATLA - eski sinyal
                                
                                # YENİ SİNYAL! İşaretlenen sete ekle
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
                                strength = whale_data['strength']
                                signal_type = whale_data['signal_type']
                                
                                # Sinyal geçmişine ekle
                                self.signal_history[symbol].append(whale_data)
                                
                                # Coin'in bugünkü sinyallerini kaydet
                                now = datetime.now()
                                if symbol not in self.coin_signals_today:
                                    self.coin_signals_today[symbol] = []
                                
                                self.coin_signals_today[symbol].append({
                                    'time': now,
                                    'signal_type': signal_type,
                                    'strength': strength
                                })
                                
                                # Eski sinyalleri temizle (24 saat önce)
                                self.coin_signals_today[symbol] = [
                                    s for s in self.coin_signals_today[symbol]
                                    if now - s['time'] < timedelta(hours=24)
                                ]
                                
                                # Son 10 sinyali tut (memory)
                                if len(self.signal_history[symbol]) > 10:
                                    self.signal_history[symbol] = self.signal_history[symbol][-10:]
                                
                                # 1️⃣ ÖNCE: HIGH/MEDIUM kontrolü
                                should_alert = False
                                alert_reason = ""
                                
                                if 'High' in strength:
                                    should_alert = True
                                    alert_reason = "⚡ HIGH STRENGTH SİNYAL!"
                                elif 'Medium' in strength:
                                    should_alert = True
                                    alert_reason = f"📊 MEDIUM {signal_type} SİNYALİ!"
                                else:
                                    # LOW - atla
                                    logger.debug(f"⏩ {symbol}: LOW sinyal atlandı")
                                    continue
                                
                                # 2️⃣ Alert gönder
                                if should_alert:
                                    self.send_alert(whale_data, alert_reason)
                                    total_alerts += 1
                                    logger.success(f"✅ {symbol}: {strength} {signal_type} → Alert gönderildi!")
                                
                                # 3️⃣ TEKRAR KONTROL: Aynı coinde 2+ sinyal var mı? (1 saat içinde)
                                recent_signals = [
                                    s for s in self.coin_signals_today[symbol]
                                    if now - s['time'] < timedelta(hours=1)
                                ]
                                
                                if len(recent_signals) >= 2:
                                    # 2+ sinyal var! Ama daha önce uyardık mı?
                                    last_repeat_alert = self.coin_repeat_alert_sent.get(symbol)
                                    
                                    # 30 dakikada bir özel uyarı gönder
                                    if last_repeat_alert is None or (now - last_repeat_alert) > timedelta(minutes=30):
                                        # ÖZEL UYARI: Aynı coinde tekrar sinyal!
                                        self.send_repeat_signal_alert(symbol, recent_signals, whale_data)
                                        self.coin_repeat_alert_sent[symbol] = now
                                        logger.success(f"🔥 {symbol}: 2+ TEKRAR SİNYAL UYARISI GÖNDERİLDİ!")
                        
                        except Exception as e:
                            continue
                    
                    # 2 saniye bekle
                    time.sleep(2)
                    
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
    logger.info(f"""
╔══════════════════════════════════════════════════════════════╗
║      🐋 WHALEHUNTER VERİ AKIŞI - SÜREKLİ İZLEME 🐋        ║
╚══════════════════════════════════════════════════════════════╝

📊 Özellikler:
  • HIGH sinyal → 8 bip (kırmızı/sarı) - ANINDA
  • MEDIUM sinyal → 2 bip (beyaz) - ANINDA
  • Aynı coinde 2+ sinyal (1 saat) → 10 bip ÖZEL UYARI
  • Sürekli veri çekme - hiç durmaz!
  • TÜM coinler izleniyor

🎯 Kullanım:
  • Konsol açık kalsın - her sinyal anında görünür
  • Chrome penceresi AÇIK KALSIN (WhaleHunter)
  • Ctrl+C ile durdur
    """)
    
    bot = WhaleAlertBot()
    
    try:
        bot.setup_driver()
        bot.login()
        bot.go_to_futures_page()
        bot.monitor_whales(duration_minutes=0)  # Sonsuz
    except Exception as e:
        logger.error(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.close()


if __name__ == "__main__":
    main()
