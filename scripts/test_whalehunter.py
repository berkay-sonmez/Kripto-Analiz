"""
WhaleHunter Bağlantı Testi
whalehunterapp.com'a bağlanıp veri çekmeyi test eder
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from src.whalehunter.wh_client import WhaleHunterClient, WhaleHunterScraper

load_dotenv()


async def test_whalehunter():
    """WhaleHunter bağlantısını test et"""
    
    print("=" * 80)
    print("🐋 WHALEHUNTER BAĞLANTI TESTİ")
    print("=" * 80)
    print()
    
    # Bilgileri al
    email = os.getenv("WHALEHUNTER_EMAIL")
    password = os.getenv("WHALEHUNTER_PASSWORD")
    
    if not email or not password or "sizin" in email.lower():
        print("❌ WhaleHunter bilgileri .env dosyasında bulunamadı!")
        print()
        print("💡 .env dosyasını düzenleyin:")
        print("   notepad .env")
        print()
        print("   Ekleyin:")
        print("   WHALEHUNTER_EMAIL=your_email@domain.com")
        print("   WHALEHUNTER_PASSWORD=your_password")
        print()
        return
    
    print(f"📧 Email: {email}")
    print(f"🔐 Şifre: {'*' * len(password)}")
    print()
    
    # API Client'ı dene
    print("🔍 Yöntem 1: API Client ile bağlanılıyor...")
    print("-" * 80)
    
    client = WhaleHunterClient(email=email, password=password)
    
    login_success = await client.login()
    
    if login_success:
        print("✅ API Login başarılı!")
        print()
        
        # Whale movements çek
        print("🐋 Whale hareketleri çekiliyor...")
        movements = await client.fetch_whale_movements()
        
        if movements:
            print(f"✅ {len(movements)} whale hareketi çekildi")
            print()
            print("📊 İlk 5 hareket:")
            for i, move in enumerate(movements[:5], 1):
                print(f"{i}. {move}")
        else:
            print("⚠️  Whale hareketi bulunamadı veya endpoint farklı")
        
        print()
        
        # Signals çek
        print("📡 Sinyaller çekiliyor...")
        signals = await client.get_signals()
        
        if signals:
            print(f"✅ {len(signals)} sinyal çekildi")
        else:
            print("⚠️  Sinyal bulunamadı")
        
    else:
        print("❌ API Login başarısız")
        print()
        print("🔍 Yöntem 2: Web Scraping deneniyor...")
        print("-" * 80)
        
        # Web scraper dene
        scraper = WhaleHunterScraper(email=email, password=password)
        
        cookies = await scraper.login_and_get_cookies()
        
        if cookies:
            print("✅ Web Login başarılı!")
            print()
            
            # Data scrape et
            print("📊 Dashboard verisi scrape ediliyor...")
            html_data = await scraper.scrape_whale_data()
            
            if html_data:
                print(f"✅ {len(html_data)} byte veri scrape edildi")
                print()
                print("💡 HTML verisi başarıyla çekildi.")
                print("   Veriyi parse etmek için BeautifulSoup kullanılabilir.")
            else:
                print("❌ Scraping başarısız")
        else:
            print("❌ Web Login başarısız")
    
    print()
    print("=" * 80)
    print()
    print("💡 Sonraki Adımlar:")
    print()
    print("1. WhaleHunter hesabınızın aktif olduğundan emin olun")
    print("2. Email ve şifrenin doğru olduğunu kontrol edin")
    print("3. WhaleHunter'da 2FA (iki faktörlü doğrulama) varsa devre dışı bırakın")
    print("4. WhaleHunter'ın API dokümantasyonunu kontrol edin")
    print()
    print("🌐 WhaleHunter Dashboard: https://whalehunterapp.com/dashboard")
    print()


if __name__ == "__main__":
    asyncio.run(test_whalehunter())
