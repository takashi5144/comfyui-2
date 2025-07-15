# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-01-15

### Fixed
- 初期データ読み込みエラーの修正
  - API呼び出しの個別エラーハンドリング追加
  - レスポンスデータの検証強化
  - インポートパスの修正（.js拡張子を明示）
- フォールバック処理の改善

## [1.0.1] - 2025-01-15

### Added
- 完全なサンプラーリスト（26種類）
  - Euler系、DPM系、DPM++系、その他高度なサンプラー
- 完全なスケジューラーリスト（20種類）
  - 基本、一様分布、Align Your Steps、高度なスケジューラー
- サンプラー/スケジューラーのカテゴリー分類と説明
- `samplers_config.py` による設定管理

### Fixed
- Tailwind CSS `resize-vertical` エラーを修正
- ESモジュール警告を修正

## [1.0.0] - 2025-01-15

### Added
- 初回リリース
- ComfyUIバックエンドとの統合
- A1111風のユーザーインターフェース
- Text to Image (txt2img) 機能
- Image to Image (img2img) 機能
- Inpainting 機能
- リアルタイム進捗表示
- モデル選択機能
- サンプラー・スケジューラー設定
- バッチ生成対応
- 画像プレビュー機能
- マスクエディタ（Inpaint用）

### Technical Stack
- Backend: FastAPI + Python
- Frontend: React + Vite + Tailwind CSS
- Image Generation: ComfyUI API