@echo off
echo ====================================
echo サービス状態確認スクリプト
echo ====================================
echo.

REM ComfyUIの確認
echo [1/3] ComfyUIの確認...
curl -s http://127.0.0.1:8188 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ ComfyUI is running on port 8188
) else (
    echo ✗ ComfyUI is NOT running
    echo   Please run ComfyUI first:
    echo   cd C:\pinokio\api\comfyui.git\app
    echo   python main.py
)

echo.

REM バックエンドAPIの確認
echo [2/3] バックエンドAPIの確認...
curl -s http://127.0.0.1:8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend API is running on port 8000
    curl -s http://127.0.0.1:8000/api/health
    echo.
) else (
    echo ✗ Backend API is NOT running
    echo   Please run: start_backend.bat
)

echo.

REM フロントエンドの確認
echo [3/3] フロントエンドの確認...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is running on port 3000
) else (
    echo ✗ Frontend is NOT running
    echo   Please run: start_frontend.bat
)

echo.
echo ====================================
pause