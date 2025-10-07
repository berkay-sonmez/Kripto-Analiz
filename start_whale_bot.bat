@echo off
REM ════════════════════════════════════════════════════════
REM 🐋 WhaleHunter Veri Akışı - Sürekli İzleme
REM ════════════════════════════════════════════════════════

cd /d "C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz"

cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      🐋 WHALEHUNTER VERİ AKIŞI - SÜREKLİ İZLEME 🐋       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📊 ÖZELLİKLER:
echo   • HIGH sinyal → 8 bip (kırmızı/sarı) - ANINDA
echo   • MEDIUM sinyal → 2 bip (beyaz) - ANINDA
echo   • 2+ sinyal (aynı coin, 1 saat) → 10 bip ÖZEL UYARI
echo   • TÜM COINLER izleniyor (filtre yok)
echo   • Sürekli veri çekme - hiç durmaz!
echo.
echo ⚠️  ÖNEMLİ:
echo   • Chrome penceresi açılacak - KAPATMAYIN!
echo   • Her sinyal anında alert verir
echo   • Konsol açık kalsın - burada görünür
echo.
echo 🛑 Durdurmak için: Ctrl+C veya bu pencereyi kapatın
echo.
echo ══════════════════════════════════════════════════════════════
echo.
echo 🚀 Bot başlatılıyor...
echo.

call .venv\Scripts\activate.bat
python scripts\whale_alert_bot_v2.py

echo.
echo 🛑 Bot durduruldu.
echo.
pause
