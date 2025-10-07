# ====================================================
# Whale Alert Bot - PowerShell Otomatik Başlatma
# ====================================================

$WorkDir = "C:\Users\berka\OneDrive\Masaüstü\Kripto-Analiz"
$PythonExe = "$WorkDir\.venv\Scripts\python.exe"
$BotScript = "$WorkDir\scripts\whale_alert_bot.py"

Write-Host ""
Write-Host "🐋 Whale Alert Bot Başlatılıyor..." -ForegroundColor Cyan
Write-Host ""

# Minimize pencerede başlat
Start-Process -FilePath $PythonExe -ArgumentList $BotScript -WindowStyle Minimized

Start-Sleep -Seconds 2

Write-Host "✅ Bot başlatıldı!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Bot arka planda çalışıyor" -ForegroundColor Yellow
Write-Host "🔊 Alert geldiğinde bip sesi duyacaksınız" -ForegroundColor Yellow
Write-Host "🛑 Durdurmak için Task Manager'dan python.exe'yi kapatın" -ForegroundColor Red
Write-Host ""
Write-Host "💡 Task Manager'ı açmak için: Ctrl+Shift+Esc" -ForegroundColor Gray
Write-Host ""
