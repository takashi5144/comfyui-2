#!/bin/bash

# デプロイスクリプト
echo "🚀 ComfyUI A1111-Style UI デプロイスクリプト"
echo "=========================================="

# 色の定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 関数定義
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Git状態確認
echo "📋 Git状態を確認中..."
if ! git diff-index --quiet HEAD --; then
    print_warning "コミットされていない変更があります"
    read -p "続行しますか？ (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# バージョン確認
CURRENT_VERSION=$(cat VERSION)
echo "現在のバージョン: v$CURRENT_VERSION"
read -p "新しいバージョンを入力 (現在: $CURRENT_VERSION): " NEW_VERSION

if [ ! -z "$NEW_VERSION" ] && [ "$NEW_VERSION" != "$CURRENT_VERSION" ]; then
    echo $NEW_VERSION > VERSION
    git add VERSION
    git commit -m "Bump version to v$NEW_VERSION"
    git tag -a "v$NEW_VERSION" -m "Version $NEW_VERSION"
    print_success "バージョンを v$NEW_VERSION に更新しました"
fi

# デプロイ先選択
echo ""
echo "デプロイ先を選択してください:"
echo "1) Vercel (フロントエンドのみ)"
echo "2) Railway (バックエンドのみ)"
echo "3) Render (フルスタック)"
echo "4) VPS (Docker Compose)"
echo "5) すべて"
read -p "選択 (1-5): " DEPLOY_TARGET

# GitHubへプッシュ
echo ""
echo "📤 GitHubへプッシュ中..."
git push origin main --tags
print_success "GitHubへのプッシュ完了"

case $DEPLOY_TARGET in
    1)
        echo "🔷 Vercelへデプロイ中..."
        print_warning "Vercelダッシュボードで自動デプロイが開始されます"
        print_warning "https://vercel.com/dashboard"
        ;;
    2)
        echo "🚂 Railwayへデプロイ中..."
        if command -v railway &> /dev/null; then
            railway up
        else
            print_warning "Railway CLIがインストールされていません"
            print_warning "https://railway.app/dashboard でデプロイしてください"
        fi
        ;;
    3)
        echo "🎨 Renderへデプロイ中..."
        print_warning "Renderダッシュボードで自動デプロイが開始されます"
        print_warning "https://dashboard.render.com"
        ;;
    4)
        echo "🖥️ VPSへデプロイ中..."
        read -p "VPSのホスト名: " VPS_HOST
        read -p "SSHユーザー名: " VPS_USER
        
        ssh $VPS_USER@$VPS_HOST << 'ENDSSH'
            cd /opt/comfyui-a1111
            git pull origin main
            docker-compose -f docker-compose.production.yml down
            docker-compose -f docker-compose.production.yml up -d --build
            docker system prune -f
ENDSSH
        print_success "VPSへのデプロイ完了"
        ;;
    5)
        echo "🌐 すべての環境へデプロイ中..."
        print_warning "各プラットフォームで自動デプロイが開始されます"
        ;;
esac

echo ""
echo "✨ デプロイプロセスが開始されました"
echo ""
echo "📊 デプロイ状況の確認:"
echo "- GitHub Actions: https://github.com/takashi5144/comfyui-2/actions"
echo "- Vercel: https://vercel.com/dashboard"
echo "- Railway: https://railway.app/dashboard"
echo "- Render: https://dashboard.render.com"