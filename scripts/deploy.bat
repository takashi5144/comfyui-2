@echo off
echo =====================================
echo ComfyUI A1111-Style UI Deploy Script
echo =====================================
echo.

REM Git状態確認
echo Checking Git status...
git status --porcelain > nul
if %errorlevel% neq 0 (
    echo [WARNING] Uncommitted changes detected
    set /p CONTINUE="Continue? (y/N): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

REM バージョン確認
set /p CURRENT_VERSION=<VERSION
echo Current version: v%CURRENT_VERSION%
set /p NEW_VERSION="Enter new version (current: %CURRENT_VERSION%): "

if not "%NEW_VERSION%"=="" (
    if not "%NEW_VERSION%"=="%CURRENT_VERSION%" (
        echo %NEW_VERSION% > VERSION
        git add VERSION
        git commit -m "Bump version to v%NEW_VERSION%"
        git tag -a "v%NEW_VERSION%" -m "Version %NEW_VERSION%"
        echo Version updated to v%NEW_VERSION%
    )
)

REM GitHubへプッシュ
echo.
echo Pushing to GitHub...
git push origin main --tags
if %errorlevel% equ 0 (
    echo Successfully pushed to GitHub
) else (
    echo Failed to push to GitHub
    exit /b 1
)

echo.
echo =====================================
echo Deployment initiated!
echo =====================================
echo.
echo Check deployment status:
echo - GitHub Actions: https://github.com/takashi5144/comfyui-2/actions
echo - Vercel: https://vercel.com/dashboard
echo - Railway: https://railway.app/dashboard
echo - Render: https://dashboard.render.com
echo.
echo For manual deployment:
echo 1. Vercel: Import from GitHub repository
echo 2. Railway: New Project -^> Deploy from GitHub
echo 3. Render: New -^> Web Service from GitHub
echo.
pause