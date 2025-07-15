# ComfyUI-A1111-UI 起動ガイド

## 必要な準備

1. **ComfyUI** が `C:\pinokio\api\comfyui.git\app` にインストールされていること
2. **Python 3.8以上** がインストールされていること
3. **Node.js 16以上** がインストールされていること

## 起動手順

### ステップ1: ComfyUIを起動

1. コマンドプロンプトを開く
2. 以下のコマンドを実行：
   ```cmd
   cd C:\pinokio\api\comfyui.git\app
   python main.py
   ```
3. `Starting server` というメッセージが表示されたら成功
4. ブラウザで http://127.0.0.1:8188 にアクセスしてComfyUIが表示されることを確認

### ステップ2: バックエンドAPIサーバーを起動

1. **新しい**コマンドプロンプトを開く（ComfyUIはそのまま起動したままにする）
2. 以下のコマンドを実行：
   ```cmd
   cd C:\Users\pokot\ComfyUI-A1111-UI
   start_backend.bat
   ```
3. `Uvicorn running on http://0.0.0.0:8000` というメッセージが表示されたら成功
4. ブラウザで http://127.0.0.1:8000 にアクセスして以下が表示されることを確認：
   ```json
   {"message":"ComfyUI A1111-Style API Server","status":"running"}
   ```

### ステップ3: フロントエンドを起動

1. **新しい**コマンドプロンプトを開く（ComfyUIとバックエンドはそのまま起動したままにする）
2. 以下のコマンドを実行：
   ```cmd
   cd C:\Users\pokot\ComfyUI-A1111-UI
   start_frontend.bat
   ```
3. `Local: http://localhost:3000/` というメッセージが表示されたら成功
4. ブラウザで http://localhost:3000 にアクセス

## トラブルシューティング

### 「サーバーに接続できません」エラーが出る場合

1. **3つのプロセスがすべて起動していることを確認**
   - ComfyUI (ポート8188)
   - バックエンドAPI (ポート8000)
   - フロントエンド (ポート3000)

2. **ポートが使用されていないか確認**
   ```cmd
   netstat -ano | findstr :8188
   netstat -ano | findstr :8000
   netstat -ano | findstr :3000
   ```

3. **ファイアウォールの設定を確認**
   - Windows Defenderファイアウォールで上記のポートが許可されているか確認

4. **ブラウザの開発者ツールでエラーを確認**
   - F12キーを押してコンソールタブを開く
   - 赤いエラーメッセージを確認

### モデルが表示されない場合

1. A1111からモデルをコピー：
   ```cmd
   cd C:\Users\pokot\ComfyUI-A1111-UI\scripts
   copy_models.bat
   ```
   オプション8（all）を選択してすべてのモデルをコピー

2. ComfyUIを再起動

### 画像生成がエラーになる場合

1. バックエンドのコンソールでエラーメッセージを確認
2. `[ERROR]`で始まるメッセージを探す
3. ComfyUIが正常に動作しているか確認

## 正常に起動した場合の確認項目

- [ ] http://127.0.0.1:8188 でComfyUIが表示される
- [ ] http://127.0.0.1:8000 でAPIサーバーのメッセージが表示される
- [ ] http://localhost:3000 でA1111風のUIが表示される
- [ ] モデルのドロップダウンにモデルが表示される
- [ ] サンプラーのドロップダウンに26種類のサンプラーが表示される

## 終了方法

1. 各コマンドプロンプトで `Ctrl + C` を押して終了
2. 終了順序：フロントエンド → バックエンド → ComfyUI