"""
WhaleHunter WebSocket test scripti
30 saniye boyunca whale verilerini dinle
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

from src.whalehunter.ws_client import WhaleHunterWSClient
from src.config.my_watchlist import MY_WATCHLIST
from loguru import logger

async def on_whale_signal(whale_entry: dict):
    """
    Whale sinyali geldiğinde çağrılan callback
    """
    logger.info(f"""
🐋 WHALE SİNYALİ ALINDI:
   Symbol: {whale_entry['symbol']}
   Type: {whale_entry['signal_type']}
   Price: ${whale_entry['price']:,.2f}
   Strength: {whale_entry['strength_label']} ({whale_entry['signal_strength']:.2f}%)
   Volume: ${whale_entry['volume_usdt']:,.0f}
   24h Change: {whale_entry['price_change_24h']:.2f}%
    """)

async def main():
    logger.info("🚀 WhaleHunter WebSocket testi başlatılıyor...")
    logger.info("⏱️  30 saniye boyunca whale verileri dinlenecek\n")
    
    email = os.getenv("WHALEHUNTER_EMAIL")
    password = os.getenv("WHALEHUNTER_PASSWORD")
    
    # WebSocket client oluştur (authenticated)
    ws_client = WhaleHunterWSClient(email=email, password=password, on_whale_signal=on_whale_signal)
    
    try:
        # 30 saniye dinle
        await ws_client.connect_and_listen(duration_seconds=30)
        
    except KeyboardInterrupt:
        logger.info("\n⏹️  Kullanıcı tarafından durduruldu")
        ws_client.stop()
    
    # Sonuçları analiz et
    logger.info("\n" + "="*60)
    logger.info("📊 TOPLAM İSTATİSTİKLER")
    logger.info("="*60)
    
    all_data = ws_client.get_whale_data()
    logger.info(f"Toplam whale sinyali: {len(all_data)}")
    
    if all_data:
        # Top 10 whale
        logger.info("\n🏆 EN GÜÇLÜ 10 WHALE SİNYALİ:")
        top_whales = ws_client.get_top_whales(limit=10)
        for idx, whale in enumerate(top_whales, 1):
            logger.info(f"{idx}. {whale['symbol']} - {whale['signal_type']} - "
                       f"Güç: {whale['signal_strength']:.2f}% - "
                       f"Hacim: ${whale['volume_usdt']:,.0f}")
        
        # Watchlist'teki coinler
        logger.info(f"\n📋 WATCHLİST'TEKİ COİNLER ({len(MY_WATCHLIST)} coin):")
        watchlist_whales = ws_client.filter_by_symbol(MY_WATCHLIST)
        
        if watchlist_whales:
            logger.info(f"✅ {len(watchlist_whales)} whale sinyali bulundu:")
            for whale in watchlist_whales:
                logger.info(f"  • {whale['symbol']} - {whale['signal_type']} - "
                           f"Güç: {whale['signal_strength']:.2f}%")
        else:
            logger.info("❌ Watchlist'teki coinler için henüz whale sinyali yok")
        
        # Signal type dağılımı
        long_count = sum(1 for w in all_data if w['signal_type'] == 'LONG')
        short_count = sum(1 for w in all_data if w['signal_type'] == 'SHORT')
        
        logger.info(f"\n📈 SİNYAL DAĞILIMI:")
        logger.info(f"  LONG:  {long_count} ({long_count/len(all_data)*100:.1f}%)")
        logger.info(f"  SHORT: {short_count} ({short_count/len(all_data)*100:.1f}%)")
        
        # Strength dağılımı
        low = sum(1 for w in all_data if w['strength_label'] == 'Low')
        medium = sum(1 for w in all_data if w['strength_label'] == 'Medium')
        high = sum(1 for w in all_data if w['strength_label'] == 'High')
        
        logger.info(f"\n💪 GÜÇ DAĞILIMI:")
        logger.info(f"  Low:    {low} ({low/len(all_data)*100:.1f}%)")
        logger.info(f"  Medium: {medium} ({medium/len(all_data)*100:.1f}%)")
        logger.info(f"  High:   {high} ({high/len(all_data)*100:.1f}%)")
        
        # Verileri kaydet
        output_dir = Path(project_root) / "data"
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "whalehunter_websocket_data.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n💾 Veriler kaydedildi: {output_file}")
    
    else:
        logger.warning("⚠️  Hiç whale verisi alınamadı")

if __name__ == "__main__":
    asyncio.run(main())
