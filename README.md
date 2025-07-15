# ComfyUI A1111-Style Interface

ComfyUIのパワフルなバックエンドに、AUTOMATIC1111風の使いやすいインターフェースを組み合わせた画像生成システムです。

## 特徴

- 📊 シンプルなタブ形式のUI (A1111風)
- 🚀 ComfyUIの高速で効率的なバックエンド
- 🎨 Text2Image、Img2Img、Inpaintingなどの基本機能
- 🔧 LoRA、ControlNetなどの高度な機能サポート
- 💾 設定の保存・読み込み機能
- 🎯 26種類のサンプラーと20種類のスケジューラー
- 🔄 A1111からのモデル自動コピー機能

## システム要件

- Python 3.8以上
- Node.js 16以上
- ComfyUI (起動済み)
- 4GB以上のVRAM推奨

## インストール

### 前提条件
- ComfyUI: `C:\pinokio\api\comfyui.git\app` にインストール済み
- A1111: `C:\Users\pokot\OneDrive\ドキュメント\A1111 Web UI Autoinstaller` にインストール済み

### セットアップ手順

1. このリポジトリをクローン
```bash
git clone https://github.com/takashi5144/comfyui-2.git
cd ComfyUI-A1111-UI
```

2. バックエンドのセットアップ
```bash
cd backend
pip install -r requirements.txt
```

3. フロントエンドのセットアップ
```bash
cd ../frontend
npm install
```

## 使用方法

### クイックスタート（バッチファイル使用）

1. A1111からモデルをコピー（初回のみ）
```batch
cd scripts
copy_models.bat
```

2. ComfyUIを起動（ポート8188）
```bash
cd C:\pinokio\api\comfyui.git\app
python main.py
```

3. バックエンドAPIサーバーを起動
```batch
start_backend.bat
```

4. フロントエンドを起動
```batch
start_frontend.bat
```

5. ブラウザで http://localhost:3000 を開く

### 手動起動

1. バックエンドAPIサーバーを起動
```bash
cd backend
python main.py
```

2. フロントエンドを起動
```bash
cd frontend
npm run dev
```

## トラブルシューティング

### 「ネットワークエラー」が発生する場合

1. ComfyUIが起動しているか確認
   - http://localhost:8188 にアクセスできることを確認

2. バックエンドが起動しているか確認
   - http://localhost:8000 にアクセスして `{"message":"ComfyUI A1111-Style API Server","status":"running"}` が表示されることを確認

3. ブラウザの開発者ツール（F12）でコンソールログを確認
   - エラーの詳細が表示されます

4. バックエンドのコンソールでエラーログを確認
   - `[ERROR]` で始まるメッセージを確認

### モデルが表示されない場合

1. `scripts/copy_models.bat` を実行してA1111からモデルをコピー
2. ComfyUIを再起動

## プロジェクト構造

```
ComfyUI-A1111-UI/
├── backend/                # FastAPIバックエンド
│   ├── main.py            # メインAPIサーバー
│   ├── comfyui_bridge.py  # ComfyUI通信ブリッジ
│   ├── workflow_manager.py # ワークフロー管理
│   └── requirements.txt   # Python依存関係
├── frontend/              # Reactフロントエンド
│   ├── src/
│   │   ├── components/    # UIコンポーネント
│   │   ├── api/          # API通信
│   │   └── App.jsx       # メインアプリ
│   └── package.json      # npm依存関係
└── workflows/            # ComfyUIワークフローテンプレート
    ├── txt2img.json
    ├── img2img.json
    └── inpaint.json
```

## ライセンス

MIT License