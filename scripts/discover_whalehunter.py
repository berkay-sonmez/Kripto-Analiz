"""
WhaleHunter endpoint keşif scripti
Authenticated olarak tüm sayfaları ve API'leri tara
"""
import asyncio
import json
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# .env dosyasını yükle
load_dotenv()

from src.whalehunter.wh_client import WhaleHunterScraper
from loguru import logger

async def main():
    logger.info("🔍 WhaleHunter endpoint keşfi başlatılıyor...")
    
    email = os.getenv("WHALEHUNTER_EMAIL")
    password = os.getenv("WHALEHUNTER_PASSWORD")
    
    if not email or not password:
        logger.error("❌ .env dosyasında WHALEHUNTER_EMAIL ve WHALEHUNTER_PASSWORD gerekli!")
        return
    
    scraper = WhaleHunterScraper(email, password)
    
    # 1. Sayfaları tara
    logger.info("\n📄 Sayfalar taranıyor...")
    page_results = await scraper.scrape_whale_data()
    
    if page_results:
        logger.info(f"\n✅ {len(page_results)} sayfa bulundu:")
        for url, info in page_results.items():
            if info['type'] == 'json':
                logger.info(f"  🔹 {url} (JSON)")
                print(json.dumps(info['data'], indent=2)[:500])
            else:
                logger.info(f"  🔹 {url} (HTML, {info['length']} bytes)")
                # HTML'de veri var mı kontrol et
                html = info['data']
                if 'whale' in html.lower() or 'volume' in html.lower() or 'signal' in html.lower():
                    logger.info(f"    ✅ İlgili içerik bulundu!")
                if 'No data available' in html:
                    logger.warning(f"    ⚠️  Boş tablo")
    else:
        logger.warning("❌ Hiç sayfa bulunamadı")
    
    # 2. API endpoint'lerini dene
    logger.info("\n🔌 API endpoint'ler taranıyor...")
    api_results = await scraper.find_api_endpoints()
    
    if api_results:
        logger.info(f"\n✅ {len(api_results)} API bulundu:")
        for api in api_results:
            logger.info(f"  🔹 {api['url']}")
            logger.info(f"     Status: {api['status']}")
            logger.info(f"     Sample: {api['data_sample']}")
    else:
        logger.warning("❌ Hiç API bulunamadı")
    
    # 3. Network trafiğine bakılması gereken durumda tavsiye
    logger.info("\n💡 Sonuç:")
    if not page_results and not api_results:
        logger.warning("""
⚠️  WhaleHunter endpoint'leri bulunamadı.
        
Öneriler:
1. Browser'da whalehunterapp.com'a giriş yap
2. F12 ile Developer Tools'u aç
3. Network sekmesine git
4. Sayfayı yenile ve whale verilerini gör
5. Network'te XHR/Fetch request'lerini incele
6. Hangi URL'lere istek atıldığını not et

Alternatif olarak:
- HTML scraping (BeautifulSoup ile table parse)
- Selenium ile browser automation
- Başka bir whale tracking servisi kullanımı
        """)

if __name__ == "__main__":
    asyncio.run(main())
