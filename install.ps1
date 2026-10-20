# 無影手一鍵安裝腳本（PowerShell）
# 在辰迅雲1上運行：打開 PowerShell，複製整段命令貼上執行

Write-Host "=== 無影手安裝 ===" -ForegroundColor Green

# 1. 克隆倉庫
Write-Host "`n[1] 克隆倉庫..." -ForegroundColor Cyan
if (Test-Path "ai-shadowless-hand") {
    Write-Host "  倉庫已存在，更新中..." -ForegroundColor Yellow
    Set-Location ai-shadowless-hand
    git pull
} else {
    git clone https://github.com/blaze-luan/ai-shadowless-hand.git
    Set-Location ai-shadowless-hand
}

# 2. 安裝依賴
Write-Host "`n[2] 安裝依賴..." -ForegroundColor Cyan
pip install -r requirements.txt

# 3. 驗證安裝
Write-Host "`n[3] 驗證安裝..." -ForegroundColor Cyan
if (Test-Path "shadowless") {
    Write-Host "  ✅ 核心模組已就緒" -ForegroundColor Green
} else {
    Write-Host "  ❌ 安裝失敗，shadowless 目錄不存在" -ForegroundColor Red
    exit 1
}

# 4. 運行演示
Write-Host "`n[4] 運行基礎演示..." -ForegroundColor Cyan
python examples/basic_usage.py

Write-Host "`n[5] 運行電眼演示..." -ForegroundColor Cyan
python examples/electric_eye_demo.py

Write-Host "`n=== 安裝完成 ===" -ForegroundColor Green
Write-Host "請按任意鍵退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")