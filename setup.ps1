# Kripto Analiz Botu - Python Kurulum Scripti
# Bu script Python kurulumu sonrası tüm adımları otomatik yapar

Write-Host "🚀 Kripto Analiz Botu Kurulumu Başlıyor..." -ForegroundColor Cyan
Write-Host ""

# Python kontrolü
Write-Host "🔍 Python kontrol ediliyor..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Host "❌ Python bulunamadı!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Lütfen Python'u yükleyin:" -ForegroundColor Yellow
    Write-Host "1. https://www.python.org/downloads/ adresine gidin" -ForegroundColor White
    Write-Host "2. Python 3.8 veya üzerini indirin" -ForegroundColor White
    Write-Host "3. Kurulum sırasında 'Add Python to PATH' seçeneğini işaretleyin" -ForegroundColor White
    Write-Host "4. Bu scripti tekrar çalıştırın" -ForegroundColor White
    Write-Host ""
    Read-Host "Devam etmek için Enter'a basın"
    exit
}

$pythonVersion = & python --version
Write-Host "✅ Python bulundu: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Virtual environment oluştur
Write-Host "📦 Virtual environment oluşturuluyor..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "✅ Virtual environment oluşturuldu" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Virtual environment zaten mevcut" -ForegroundColor Cyan
}
Write-Host ""

# Virtual environment aktive et
Write-Host "🔌 Virtual environment aktive ediliyor..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# pip güncelle
Write-Host "⬆️  pip güncelleniyor..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✅ pip güncellendi" -ForegroundColor Green
Write-Host ""

# Bağımlılıkları yükle
Write-Host "📚 Bağımlılıklar yükleniyor (bu biraz zaman alabilir)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✅ Tüm bağımlılıklar yüklendi" -ForegroundColor Green
Write-Host ""

# .env dosyası kontrolü
Write-Host "🔐 Yapılandırma kontrol ediliyor..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "⚠️  .env dosyası oluşturuldu" -ForegroundColor Yellow
    Write-Host "Lütfen .env dosyasını düzenleyin ve TradingView bilgilerinizi girin:" -ForegroundColor White
    Write-Host "  notepad .env" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host "✅ .env dosyası mevcut" -ForegroundColor Green
}
Write-Host ""

# Klasörleri kontrol et
Write-Host "📁 Klasörler kontrol ediliyor..." -ForegroundColor Yellow
$folders = @("data", "logs", "notebooks", "tests")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
    }
}
Write-Host "✅ Tüm klasörler hazır" -ForegroundColor Green
Write-Host ""

# Kurulum tamamlandı
Write-Host "🎉 Kurulum Tamamlandı!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Sonraki Adımlar:" -ForegroundColor Cyan
Write-Host "1. .env dosyasını düzenleyin:" -ForegroundColor White
Write-Host "   notepad .env" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Test çalıştırması yapın:" -ForegroundColor White
Write-Host "   python scripts\fetch_coins.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Ana botu başlatın:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Daha fazla bilgi için SETUP.md dosyasını okuyun." -ForegroundColor Yellow
Write-Host ""
