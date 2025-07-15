# ComfyUI A1111-Style Interface

ComfyUIのパワフルなバックエンドに、AUTOMATIC1111風の使いやすいインターフェースを組み合わせた画像生成システムです。

## 特徴

- 📊 シンプルなタブ形式のUI (A1111風)
- 🚀 ComfyUIの高速で効率的なバックエンド
- 🎨 Text2Image、Img2Img、Inpaintingなどの基本機能
- 🔧 LoRA、ControlNetなどの高度な機能サポート
- 💾 設定の保存・読み込み機能

## システム要件

- Python 3.8以上
- Node.js 16以上
- ComfyUI (起動済み)
- 4GB以上のVRAM推奨

## インストール

1. このリポジトリをクローン
```bash
git clone [repository-url]
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

1. ComfyUIを起動（ポート8188）
```bash
cd [ComfyUI directory]
python main.py
```

2. バックエンドAPIサーバーを起動
```bash
cd backend
python main.py
```

3. フロントエンドを起動
```bash
cd frontend
npm run dev
```

4. ブラウザで http://localhost:3000 を開く

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