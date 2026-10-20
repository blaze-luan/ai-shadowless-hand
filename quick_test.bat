@echo off
chcp 65001 >nul
echo === 無影手快速測試 ===
echo.
echo [1] 克隆倉庫...
git clone https://github.com/blaze-luan/ai-shadowless-hand.git 2>nul || (echo 倉庫已存在，更新中... && cd ai-shadowless-hand && git pull)
cd ai-shadowless-hand

echo.
echo [2] 安裝依賴...
pip install -r requirements.txt

echo.
echo [3] 運行測試...
python -m pytest tests/ -v

echo.
echo [4] 運行演示...
python examples/basic_usage.py
echo.
python examples/electric_eye_demo.py

echo.
echo === 完成 ===
pause
