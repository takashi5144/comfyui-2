@echo off
echo ====================================
echo ポート使用状況確認
echo ====================================
echo.

echo Checking port 8188 (ComfyUI)...
netstat -ano | findstr :8188
echo.

echo Checking port 8000 (Backend API)...
netstat -ano | findstr :8000
echo.

echo Checking port 3000 (Frontend)...
netstat -ano | findstr :3000
echo.

echo ====================================
echo 何か表示されている場合、そのポートは使用中です。
echo PIDを確認して、必要に応じてタスクマネージャーで終了してください。
echo ====================================

pause