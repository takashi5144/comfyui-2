@echo off
echo ====================================
echo バックエンドサーバーを起動中...
echo ====================================
echo.

cd backend
call venv\Scripts\activate
echo FastAPIサーバーを起動します...
echo URL: http://localhost:8000
echo.
python main.py

pause