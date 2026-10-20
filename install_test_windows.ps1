# Windows 一鍵測試腳本（PowerShell）
# 在辰迅雲1上以管理員權限運行

Write-Host "=== 無影手 + 電眼 測試腳本 ===" -ForegroundColor Cyan

# 1. 檢查 Python
Write-Host "`n[1/5] 檢查 Python 環境..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $python) {
    Write-Host "❌ 未找到 Python，請先安裝 Python 3.7+" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Python: $($python.Source)" -ForegroundColor Green

# 2. 克隆倉庫
Write-Host "`n[2/5] 克隆 GitHub 倉庫..." -ForegroundColor Yellow
$repoUrl = "https://github.com/blaze-luan/ai-shadowless-hand.git"
$targetDir = "$env:USERPROFILE\ai-shadowless-hand"

if (Test-Path $targetDir) {
    Write-Host "⚠ 目錄已存在，更新中..." -ForegroundColor Yellow
    Set-Location $targetDir
    git pull
} else {
    Write-Host "克隆到 $targetDir ..." -ForegroundColor Cyan
    git clone $repoUrl $targetDir
    Set-Location $targetDir
}

# 3. 安裝依賴
Write-Host "`n[3/5] 安裝 Python 依賴..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4. 運行測試
Write-Host "`n[4/5] 運行單元測試..." -ForegroundColor Yellow
python -m pytest tests/ -v

# 5. 運行示例
Write-Host "`n[5/5] 運行演示程序..." -ForegroundColor Yellow
Write-Host "`n--- 基礎功能演示 ---" -ForegroundColor Cyan
python examples/basic_usage.py

Write-Host "`n--- 電眼高級版演示 ---" -ForegroundColor Cyan
python examples/electric_eye_demo.py

Write-Host "`n=== 測試完成 ===" -ForegroundColor Green
Write-Host "倉庫位置: $targetDir" -ForegroundColor Cyan
Write-Host "GitHub: https://github.com/blaze-luan/ai-shadowless-hand" -ForegroundColor Cyan
