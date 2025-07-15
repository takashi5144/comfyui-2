@echo off
echo ====================================
echo ComfyUI A1111-Style UI セットアップ
echo ====================================
echo.

REM Pythonのバージョン確認
echo Pythonバージョンを確認中...
python --version
if errorlevel 1 (
    echo [エラー] Pythonがインストールされていません。
    echo Python 3.8以上をインストールしてください。
    pause
    exit /b 1
)

REM Node.jsのバージョン確認
echo.
echo Node.jsバージョンを確認中...
node --version
if errorlevel 1 (
    echo [エラー] Node.jsがインストールされていません。
    echo Node.js 16以上をインストールしてください。
    pause
    exit /b 1
)

REM バックエンドのセットアップ
echo.
echo ====================================
echo バックエンドのセットアップ中...
echo ====================================
cd backend
echo Python仮想環境を作成中...
python -m venv venv
if errorlevel 1 (
    echo [エラー] 仮想環境の作成に失敗しました。
    pause
    exit /b 1
)

echo 仮想環境を有効化中...
call venv\Scripts\activate

echo 必要なパッケージをインストール中...
pip install -r requirements.txt
if errorlevel 1 (
    echo [エラー] パッケージのインストールに失敗しました。
    pause
    exit /b 1
)

cd ..

REM フロントエンドのセットアップ
echo.
echo ====================================
echo フロントエンドのセットアップ中...
echo ====================================
cd frontend
echo npmパッケージをインストール中...
npm install
if errorlevel 1 (
    echo [エラー] npmパッケージのインストールに失敗しました。
    pause
    exit /b 1
)

cd ..

echo.
echo ====================================
echo セットアップが完了しました！
echo ====================================
echo.
echo 使用方法:
echo 1. ComfyUIを起動してください（ポート8188）
echo 2. start-backend.bat を実行してバックエンドを起動
echo 3. start-frontend.bat を実行してフロントエンドを起動
echo 4. ブラウザで http://localhost:3000 を開く
echo.
pause