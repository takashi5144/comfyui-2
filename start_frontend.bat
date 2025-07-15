@echo off
echo ComfyUI-A1111-UI Frontend Development Server
echo ==========================================
echo.

cd frontend

REM 依存関係のインストール
echo Installing dependencies...
call npm install

echo.
echo Starting frontend dev server...
echo Access at: http://localhost:3000
echo.

REM 開発サーバー起動
call npm run dev

pause