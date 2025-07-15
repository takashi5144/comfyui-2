# デプロイメントガイド

## ローカル開発環境

```bash
# リポジトリをクローン
git clone git@github.com:takashi5144/comfyui-2.git
cd comfyui-2

# セットアップスクリプトを実行
./setup.bat

# ComfyUIを起動（別ウィンドウ）
cd [ComfyUI directory]
python main.py

# アプリケーションを起動
./start-all.bat
```

## Docker Composeを使用したデプロイ

```bash
# Dockerイメージをビルドして起動
docker-compose up -d

# ログを確認
docker-compose logs -f

# 停止
docker-compose down
```

## 本番環境へのデプロイ

### 1. VPSまたはクラウドサーバーの準備

必要なスペック：
- CPU: 4コア以上
- RAM: 8GB以上
- GPU: NVIDIA GPU（CUDA対応）推奨
- ストレージ: 50GB以上

### 2. 環境構築

```bash
# システムを更新
sudo apt update && sudo apt upgrade -y

# Dockerをインストール
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Docker Composeをインストール
sudo apt install docker-compose-plugin

# NVIDIA Docker Toolkitをインストール（GPU使用時）
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update && sudo apt install -y nvidia-docker2
sudo systemctl restart docker
```

### 3. アプリケーションのデプロイ

```bash
# リポジトリをクローン
git clone git@github.com:takashi5144/comfyui-2.git
cd comfyui-2

# 環境変数を設定
cp backend/.env.example backend/.env
# .envファイルを編集して本番環境の設定を追加

# Dockerコンテナを起動
docker-compose -f docker-compose.production.yml up -d

# SSL証明書の設定（Let's Encrypt）
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 4. Nginxリバースプロキシ設定

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## 環境変数

### Backend (.env)
```
COMFYUI_URL=http://localhost:8188
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### Frontend
```
VITE_API_URL=https://your-domain.com/api
```

## モニタリング

```bash
# Docker統計情報
docker stats

# ログの確認
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f comfyui

# システムリソース
htop
nvidia-smi  # GPU使用時
```

## トラブルシューティング

### GPU認識されない場合
```bash
# NVIDIA Driverの確認
nvidia-smi

# Docker GPU対応確認
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

### メモリ不足エラー
```bash
# Swapファイルを追加
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### ポート競合
```bash
# 使用中のポートを確認
sudo lsof -i :8000
sudo lsof -i :3000
sudo lsof -i :8188
```