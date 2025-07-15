@echo off
echo ====================================
echo テストサーバー起動
echo ====================================
echo.
echo このサーバーはComfyUIなしで動作確認用です。
echo.

cd backend

echo Starting test server...
python test_server.py

pause