@echo off
echo ComfyUI-A1111-UI Backend Server
echo ================================
echo.

cd backend

REM Python仮想環境があれば有効化
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM 依存関係のインストール
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting backend server...
echo Access at: http://localhost:8000
echo.

REM サーバー起動
python main.py

pause