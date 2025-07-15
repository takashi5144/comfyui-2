# トラブルシューティングガイド

## 「サーバーに接続できません」エラーの解決手順

### ステップ1: 診断を実行

```cmd
diagnose.bat
```

このコマンドで以下を確認します：
- Python環境
- 必要なパッケージ
- ポートの使用状況
- ファイルの存在
- API接続

### ステップ2: テストサーバーで確認

バックエンドが起動しない場合、まずテストサーバーで確認：

```cmd
test_backend.bat
```

ブラウザで http://127.0.0.1:8000 にアクセスして、以下が表示されるか確認：
```json
{"message":"Test server is running","status":"ok"}
```

### ステップ3: 本番バックエンドのデバッグ

テストサーバーが動作する場合：

```cmd
debug_backend.bat
```

エラーメッセージを確認して、以下の対処を行います：

#### よくあるエラーと対処法

1. **`ModuleNotFoundError: No module named 'xxx'`**
   ```cmd
   cd backend
   pip install -r requirements.txt
   ```

2. **`[Errno 10048] Only one usage of each socket address`**
   - ポート8000が使用中です
   - `check_ports.bat`でPIDを確認
   - タスクマネージャーでそのプロセスを終了

3. **`ImportError: cannot import name 'xxx' from 'yyy'`**
   - パッケージのバージョン不一致
   ```cmd
   cd backend
   pip install --upgrade -r requirements.txt
   ```

### ステップ4: 手動起動で確認

すべてのサービスを手動で起動：

1. **ComfyUI**（新しいコマンドプロンプト）
   ```cmd
   cd C:\pinokio\api\comfyui.git\app
   python main.py
   ```

2. **バックエンド**（新しいコマンドプロンプト）
   ```cmd
   cd C:\Users\pokot\ComfyUI-A1111-UI\backend
   python main.py
   ```

3. **フロントエンド**（新しいコマンドプロンプト）
   ```cmd
   cd C:\Users\pokot\ComfyUI-A1111-UI\frontend
   npm run dev
   ```

### ステップ5: ブラウザでの確認

1. 開発者ツールを開く（F12）
2. コンソールタブを選択
3. ネットワークタブを選択
4. 画像生成ボタンを押す
5. 失敗したリクエストの詳細を確認

### それでも解決しない場合

1. **Windowsファイアウォールの確認**
   - コントロールパネル → Windows Defender ファイアウォール
   - 「アプリケーションの許可」でPythonを許可

2. **アンチウイルスソフトの確認**
   - 一時的に無効化して確認

3. **完全な再インストール**
   ```cmd
   cd backend
   rmdir /s /q venv
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

## エラーメッセージ別対処法

### "Network Error"
- バックエンドが起動していない → `start_backend.bat`を実行

### "CORS error"
- バックエンドのCORS設定の問題 → 最新版に更新

### "Connection refused"
- ポートが間違っている → 127.0.0.1:8000 を使用

### "Timeout"
- ComfyUIが応答していない → ComfyUIを再起動