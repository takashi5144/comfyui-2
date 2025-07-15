@echo off
echo ====================================
echo ComfyUI-A1111-UI 統合起動スクリプト
echo ====================================
echo.

REM ComfyUIの起動
echo [1/3] ComfyUIを起動しています...
start "ComfyUI" cmd /k "cd /d C:\pinokio\api\comfyui.git\app && python main.py"

REM 少し待機（ComfyUIが起動するまで）
echo ComfyUIの起動を待っています...
timeout /t 10 /nobreak

REM バックエンドの起動
echo.
echo [2/3] バックエンドAPIを起動しています...
start "Backend API" cmd /k "cd /d %~dp0 && start_backend.bat"

REM 少し待機（バックエンドが起動するまで）
echo バックエンドの起動を待っています...
timeout /t 5 /nobreak

REM フロントエンドの起動
echo.
echo [3/3] フロントエンドを起動しています...
start "Frontend" cmd /k "cd /d %~dp0 && start_frontend.bat"

echo.
echo ====================================
echo すべてのサービスを起動しました！
echo.
echo ブラウザで以下のURLにアクセスしてください：
echo http://localhost:3000
echo.
echo 終了するには各ウィンドウでCtrl+Cを押してください。
echo ====================================
echo.

REM 5秒後にブラウザを開く
timeout /t 5 /nobreak
start http://localhost:3000

pause