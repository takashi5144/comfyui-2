@echo off
echo =====================================
echo ComfyUI-A1111-UI 診断ツール
echo =====================================
echo.

echo [1] Python環境の確認
python --version
echo.

echo [2] 必要なPythonパッケージの確認
cd backend
echo Checking FastAPI...
pip show fastapi >nul 2>&1
if %errorlevel% equ 0 (echo ✓ FastAPI installed) else (echo ✗ FastAPI NOT installed)

echo Checking uvicorn...
pip show uvicorn >nul 2>&1
if %errorlevel% equ 0 (echo ✓ uvicorn installed) else (echo ✗ uvicorn NOT installed)

echo Checking aiohttp...
pip show aiohttp >nul 2>&1
if %errorlevel% equ 0 (echo ✓ aiohttp installed) else (echo ✗ aiohttp NOT installed)
cd ..
echo.

echo [3] Node.js環境の確認
node --version
npm --version
echo.

echo [4] ポート使用状況
echo Port 8000 (Backend):
netstat -ano | findstr :8000
if %errorlevel% neq 0 (echo ✓ Port 8000 is free)
echo.

echo [5] ファイル存在確認
if exist backend\main.py (echo ✓ backend\main.py exists) else (echo ✗ backend\main.py NOT found)
if exist backend\requirements.txt (echo ✓ backend\requirements.txt exists) else (echo ✗ backend\requirements.txt NOT found)
if exist frontend\package.json (echo ✓ frontend\package.json exists) else (echo ✗ frontend\package.json NOT found)
echo.

echo [6] API接続テスト
curl -s http://127.0.0.1:8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend API is responding
    curl -s http://127.0.0.1:8000
) else (
    echo ✗ Backend API is NOT responding
    echo.
    echo 推奨アクション:
    echo 1. test_backend.bat を実行してテストサーバーを起動
    echo 2. debug_backend.bat を実行してエラーを確認
)

echo.
echo =====================================
pause