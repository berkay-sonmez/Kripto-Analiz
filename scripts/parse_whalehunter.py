"""
WhaleHunter HTML parser - binance-futures sayfasından veri çek
"""
import asyncio
import json
import re
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Proje root'unu path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# .env dosyasını yükle
load_dotenv()

from src.whalehunter.wh_client import WhaleHunterScraper
from loguru import logger

async def parse_binance_futures():
    """
    binance-futures sayfasından whale verilerini parse et
    """
    email = os.getenv("WHALEHUNTER_EMAIL")
    password = os.getenv("WHALEHUNTER_PASSWORD")
    
    if not email or not password:
        logger.error("❌ .env dosyasında WHALEHUNTER_EMAIL ve WHALEHUNTER_PASSWORD gerekli!")
        return None
    
    scraper = WhaleHunterScraper(email, password)
    
    # binance-futures sayfasını çek
    results = await scraper.scrape_whale_data()
    
    if not results:
        logger.error("❌ Sayfa çekilemedi")
        return None
    
    futures_url = "https://whalehunterapp.com/binance-futures"
    
    if futures_url not in results:
        logger.error("❌ binance-futures sayfası bulunamadı")
        return None
    
    html = results[futures_url]['data']
    
    # BeautifulSoup ile parse et
    soup = BeautifulSoup(html, 'html.parser')
    
    logger.info("📊 HTML parse ediliyor...")
    
    # 1. Table'ları bul
    tables = soup.find_all('table')
    logger.info(f"  🔹 {len(tables)} tablo bulundu")
    
    whale_data = []
    
    for idx, table in enumerate(tables):
        logger.info(f"\n  📋 Tablo {idx + 1}:")
        
        # Table headers
        headers = []
        thead = table.find('thead')
        if thead:
            header_cells = thead.find_all(['th', 'td'])
            headers = [cell.get_text(strip=True) for cell in header_cells]
            logger.info(f"     Headers: {headers}")
        
        # Table rows
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
            logger.info(f"     Rows: {len(rows)}")
            
            for row_idx, row in enumerate(rows[:5]):  # İlk 5 satır
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                logger.info(f"       Row {row_idx + 1}: {row_data}")
                
                # Coin/symbol ve volume data var mı kontrol et
                if row_data:
                    whale_entry = {}
                    for i, header in enumerate(headers):
                        if i < len(row_data):
                            whale_entry[header] = row_data[i]
                    
                    if whale_entry:
                        whale_data.append(whale_entry)
    
    # 2. Script tag'larında JSON data var mı?
    scripts = soup.find_all('script')
    logger.info(f"\n  🔹 {len(scripts)} script bloğu bulundu")
    
    for script in scripts:
        script_text = script.string
        if script_text and ('whale' in script_text.lower() or 'volume' in script_text.lower()):
            # JSON benzeri data ara
            json_matches = re.findall(r'\{[^{}]*(?:"symbol"|"coin"|"volume")[^{}]*\}', script_text)
            if json_matches:
                logger.info(f"     ✅ JSON data bulundu: {len(json_matches)} entry")
                for match in json_matches[:3]:
                    logger.info(f"       {match[:100]}...")
    
    # 3. Data attribute'ları
    data_elements = soup.find_all(attrs={'data-coin': True}) + soup.find_all(attrs={'data-symbol': True})
    if data_elements:
        logger.info(f"\n  🔹 {len(data_elements)} data attribute bulundu")
    
    # 4. HTML'i kaydet (analiz için)
    output_dir = Path(project_root) / "data"
    output_dir.mkdir(exist_ok=True)
    
    html_file = output_dir / "whalehunter_page.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    logger.info(f"\n💾 HTML kaydedildi: {html_file}")
    
    # 5. Sonuçları kaydet
    if whale_data:
        output_file = output_dir / "whalehunter_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(whale_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ {len(whale_data)} whale entry kaydedildi: {output_file}")
        
        # İlk birkaç entry'yi göster
        logger.info("\n📊 İlk 3 whale entry:")
        for entry in whale_data[:3]:
            logger.info(f"  {entry}")
    else:
        logger.warning("\n⚠️  Hiç whale data parse edilemedi - sayfa muhtemelen JavaScript ile yükleniyor")
        logger.info("""
💡 Çözüm önerileri:
1. Browser'da whalehunterapp.com/binance-futures'u aç
2. F12 Developer Tools'u aç
3. Network sekmesine git, XHR/Fetch filtrele
4. Sayfayı yenile
5. Hangi API endpoint'lerine istek atıldığını not et
6. O endpoint'leri doğrudan kullanabiliriz

Alternatif: Selenium ile browser automation kullan
        """)
        
        logger.info(f"\n📄 Kaydedilen HTML dosyasını inceleyebilirsiniz: {html_file}")
    
    return whale_data

if __name__ == "__main__":
    asyncio.run(parse_binance_futures())
