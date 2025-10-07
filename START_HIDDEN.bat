@echo off
REM ════════════════════════════════════════════════════════
REM 🐋 Whale Alert Bot - Arka Plan Başlatıcı
REM ════════════════════════════════════════════════════════

cd /d "C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║      🐋 WHALE ALERT BOT - ARKA PLANDA BAŞLATILIYOR 🐋      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📊 Bot arka planda başlatılıyor...
echo 🔕 Pencere gizlenecek - görev çubuğunda görünmeyecek
echo 📱 Telegram bildirimleri aktif!
echo.
echo ⚠️  Durdurmak için: Görev Yöneticisi'nden python.exe'yi kapatın
echo.

REM Arka planda başlat (minimize ve gizli)
start "" /B /MIN cmd /c ".venv\Scripts\python.exe scripts\whale_alert_bot_v2.py >nul 2>&1"

echo ✅ Bot arka planda başlatıldı!
echo.
echo 💡 Bot çalışıyor mu kontrol: Görev Yöneticisi → Ayrıntılar → python.exe
echo.
timeout /t 5
exit
