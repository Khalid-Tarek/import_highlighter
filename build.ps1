$ErrorActionPreference = "Stop"

Write-Host "Checking for PyInstaller..." -ForegroundColor Cyan
$installed = python -m pip show pyinstaller 2>$null
if (-not $installed) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    python -m pip install pyinstaller
}

$src = Join-Path $PSScriptRoot "src" "import_highlighter.py"
if (-not (Test-Path $src)) {
    Write-Host "ERROR: $src not found" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Building executable..." -ForegroundColor Cyan
python -m PyInstaller `
    --onefile `
    --windowed `
    --name "ImportHighlighter" `
    --distpath (Join-Path $PSScriptRoot "dist") `
    --workpath (Join-Path $PSScriptRoot "dist" "build") `
    --specpath (Join-Path $PSScriptRoot "dist" "spec") `
    --noconfirm `
    $src

$exe = Join-Path $PSScriptRoot "dist" "ImportHighlighter.exe"
if (Test-Path $exe) {
    $size = [math]::Round((Get-Item $exe).Length / 1MB, 1)
    Write-Host "`nDone: $exe ($size MB)" -ForegroundColor Green
} else {
    Write-Host "`nBuild may have failed." -ForegroundColor Red
}

Read-Host "`nPress Enter to exit"
