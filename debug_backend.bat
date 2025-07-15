@echo off
echo ====================================
echo バックエンドデバッグモード起動
echo ====================================
echo.

cd backend

REM Pythonのバージョン確認
echo Python version:
python --version
echo.

REM 必要なパッケージの確認
echo Checking required packages...
pip show fastapi uvicorn aiohttp >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing missing packages...
    pip install -r requirements.txt
)

echo.
echo Starting backend in debug mode...
echo.

REM デバッグモードで起動（エラーを詳しく表示）
python -u main.py

pause