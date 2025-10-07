"""
Kripto Analiz Botu - Ana Dosya
TradingView entegrasyonu ile altcoin analizi
"""

import os
import asyncio
from dotenv import load_dotenv
from loguru import logger

from src.tradingview.tv_client import TradingViewClient
from src.analyzers.technical_analyzer import TechnicalAnalyzer
from src.utils.data_manager import DataManager

# .env dosyasını yükle
load_dotenv()

# Loglama ayarları
logger.add("logs/bot_{time}.log", rotation="1 day", retention="7 days", level="INFO")


async def main():
    """Ana bot fonksiyonu"""
    logger.info("🚀 Kripto Analiz Botu başlatılıyor...")
    
    # TradingView client oluştur
    tv_username = os.getenv("TRADINGVIEW_USERNAME")
    tv_password = os.getenv("TRADINGVIEW_PASSWORD")
    
    if not tv_username or not tv_password:
        logger.error("❌ TradingView bilgileri .env dosyasında bulunamadı!")
        logger.info("💡 .env.example dosyasını .env olarak kopyalayın ve bilgilerinizi girin.")
        return
    
    try:
        # TradingView bağlantısı
        tv_client = TradingViewClient(tv_username, tv_password)
        logger.info("✅ TradingView bağlantısı hazır")
        
        # Veri yöneticisi
        data_manager = DataManager()
        
        # Teknik analiz modülü
        analyzer = TechnicalAnalyzer()
        
        # Ana döngü
        update_interval = int(os.getenv("UPDATE_INTERVAL", 300))
        logger.info(f"🔄 Güncelleme aralığı: {update_interval} saniye")
        
        while True:
            try:
                logger.info("📊 Altcoin verileri çekiliyor...")
                
                # Tüm altcoinleri çek
                coins = await tv_client.fetch_all_altcoins()
                logger.info(f"✅ {len(coins)} altcoin çekildi")
                
                # Verileri kaydet
                data_manager.save_coins(coins)
                
                # Analiz yap
                logger.info("🔍 Teknik analiz yapılıyor...")
                signals = analyzer.analyze_batch(coins)
                
                # Sinyalleri göster
                strong_signals = [s for s in signals if s['strength'] == 'STRONG']
                if strong_signals:
                    logger.info(f"🎯 {len(strong_signals)} güçlü sinyal bulundu:")
                    for signal in strong_signals[:5]:  # İlk 5 sinyali göster
                        logger.info(f"  • {signal['symbol']}: {signal['action']} - {signal['reason']}")
                
                # Bekle
                logger.info(f"⏳ {update_interval} saniye bekleniyor...\n")
                await asyncio.sleep(update_interval)
                
            except KeyboardInterrupt:
                logger.info("⏹️  Bot durduruldu (Ctrl+C)")
                break
            except Exception as e:
                logger.error(f"❌ Hata: {e}")
                await asyncio.sleep(60)  # Hata durumunda 1 dakika bekle
                
    except Exception as e:
        logger.error(f"❌ Başlatma hatası: {e}")
        return


if __name__ == "__main__":
    asyncio.run(main())
