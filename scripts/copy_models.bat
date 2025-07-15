@echo off
echo A1111からComfyUIにモデルをコピーします
echo.

REM Python実行確認
python --version >nul 2>&1
if errorlevel 1 (
    echo エラー: Pythonがインストールされていません
    pause
    exit /b 1
)

echo 利用可能なオプション:
echo   1. checkpoints (Stable Diffusionモデル)
echo   2. vae (VAEモデル)
echo   3. loras (LoRAモデル)
echo   4. embeddings (Textual Inversion)
echo   5. hypernetworks (Hypernetworks)
echo   6. controlnet (ControlNetモデル)
echo   7. upscale (アップスケーラー)
echo   8. all (すべてのモデル)
echo   9. dry-run (実際にコピーせずに確認のみ)
echo.

set /p choice="選択してください (1-9): "

if "%choice%"=="1" (
    python copy_models_from_a1111.py checkpoints
) else if "%choice%"=="2" (
    python copy_models_from_a1111.py vae
) else if "%choice%"=="3" (
    python copy_models_from_a1111.py loras
) else if "%choice%"=="4" (
    python copy_models_from_a1111.py embeddings
) else if "%choice%"=="5" (
    python copy_models_from_a1111.py hypernetworks
) else if "%choice%"=="6" (
    python copy_models_from_a1111.py controlnet
) else if "%choice%"=="7" (
    python copy_models_from_a1111.py upscale
) else if "%choice%"=="8" (
    python copy_models_from_a1111.py all
) else if "%choice%"=="9" (
    python copy_models_from_a1111.py all --dry-run
) else (
    echo 無効な選択です
)

echo.
pause