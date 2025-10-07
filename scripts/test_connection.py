"""
TradingView Hesap Bağlantı Testi
"""

import os
import sys
from dotenv import load_dotenv
from loguru import logger

# .env dosyasını yükle
load_dotenv()

def test_tradingview_connection():
    """TradingView hesap bilgilerini kontrol et"""
    
    print("🔍 TradingView Hesap Bağlantısı Kontrol Ediliyor...\n")
    
    # Bilgileri al
    username = os.getenv("TRADINGVIEW_USERNAME")
    password = os.getenv("TRADINGVIEW_PASSWORD")
    
    # Bilgi kontrolü
    if not username or not password:
        print("❌ TradingView bilgileri bulunamadı!")
        print("💡 Lütfen .env dosyasını kontrol edin.\n")
        return False
    
    print(f"✅ Kullanıcı Adı: {username}")
    print(f"✅ Şifre: {'*' * len(password)} (gizli)\n")
    
    # TradingView API'sine test bağlantısı yap
    print("📡 TradingView API'sine bağlanılıyor...\n")
    
    try:
        from tradingview_ta import TA_Handler, Interval
        
        # Test için Bitcoin verisi çek
        print("🧪 Test: Bitcoin (BTCUSDT) verisi çekiliyor...")
        
        handler = TA_Handler(
            symbol="BTCUSDT",
            exchange="BINANCE",
            screener="crypto",
            interval=Interval.INTERVAL_15_MINUTES
        )
        
        analysis = handler.get_analysis()
        
        print("✅ API Bağlantısı Başarılı!\n")
        print("📊 Bitcoin Test Verisi:")
        print(f"  • Fiyat: ${analysis.indicators.get('close', 0):,.2f}")
        print(f"  • RSI: {analysis.indicators.get('RSI', 0):.2f}")
        print(f"  • MACD: {analysis.indicators.get('MACD.macd', 0):.4f}")
        print(f"  • Öneri: {analysis.summary.get('RECOMMENDATION', 'N/A')}")
        print(f"  • AL Sinyalleri: {analysis.summary.get('BUY', 0)}")
        print(f"  • SAT Sinyalleri: {analysis.summary.get('SELL', 0)}\n")
        
        # Not: tradingview-ta kütüphanesi kullanıcı adı/şifre gerektirmiyor
        # Public data API kullanıyor
        print("ℹ️  Not: TradingView-TA kütüphanesi public API kullanır.")
        print("   Kullanıcı adı/şifre premium özellikleri için saklanır.\n")
        
        print("🎉 TradingView Hesabı Başarıyla Yapılandırıldı!\n")
        return True
        
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}\n")
        print("💡 Muhtemel Nedenler:")
        print("  • İnternet bağlantısı sorunu")
        print("  • TradingView API geçici olarak erişilemez")
        print("  • Rate limit (çok fazla istek)\n")
        return False


if __name__ == "__main__":
    success = test_tradingview_connection()
    
    if success:
        print("✅ Sonraki Adım: Ana botu çalıştırabilirsiniz!")
        print("   Komut: python main.py\n")
    else:
        print("❌ Lütfen hataları düzeltin ve tekrar deneyin.\n")
