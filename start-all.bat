@echo off
echo ====================================
echo ComfyUI A1111-Style UI 起動スクリプト
echo ====================================
echo.

REM ComfyUIが起動しているか確認
echo ComfyUIの接続を確認中...
curl -s http://localhost:8188 > nul
if errorlevel 1 (
    echo [警告] ComfyUIが起動していません。
    echo 先にComfyUIを起動してください。
    echo.
    pause
)

echo バックエンドとフロントエンドを起動します...
echo.

REM 新しいウィンドウでバックエンドを起動
start "ComfyUI A1111 Backend" cmd /k start-backend.bat

REM 少し待機
timeout /t 3 /nobreak > nul

REM 新しいウィンドウでフロントエンドを起動
start "ComfyUI A1111 Frontend" cmd /k start-frontend.bat

echo.
echo ====================================
echo 起動処理が完了しました
echo ====================================
echo.
echo しばらく待ってから以下のURLにアクセスしてください:
echo http://localhost:3000
echo.
echo 終了するには、各ウィンドウでCtrl+Cを押してください。
echo.
pause