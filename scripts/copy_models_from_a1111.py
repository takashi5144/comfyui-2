#!/usr/bin/env python3
"""
A1111からComfyUIにモデルをコピーするスクリプト
"""

import os
import shutil
import sys
from pathlib import Path
import json

# デフォルトパス設定
A1111_PATH = r"C:\Users\pokot\OneDrive\ドキュメント\A1111 Web UI Autoinstaller"
COMFYUI_PATH = r"C:\pinokio\api\comfyui.git\app"

# モデルタイプとディレクトリのマッピング
MODEL_MAPPINGS = {
    "checkpoints": {
        "src": "models/Stable-diffusion",
        "dst": "models/checkpoints",
        "extensions": [".ckpt", ".safetensors", ".pt", ".pth"]
    },
    "vae": {
        "src": "models/VAE",
        "dst": "models/vae",
        "extensions": [".ckpt", ".safetensors", ".pt", ".pth"]
    },
    "loras": {
        "src": "models/Lora",
        "dst": "models/loras",
        "extensions": [".safetensors", ".pt", ".pth"]
    },
    "embeddings": {
        "src": "embeddings",
        "dst": "models/embeddings",
        "extensions": [".pt", ".pth", ".safetensors", ".bin"]
    },
    "hypernetworks": {
        "src": "models/hypernetworks",
        "dst": "models/hypernetworks",
        "extensions": [".pt", ".pth", ".safetensors"]
    },
    "controlnet": {
        "src": "models/ControlNet",
        "dst": "models/controlnet",
        "extensions": [".safetensors", ".pth"]
    },
    "upscale": {
        "src": "models/ESRGAN",
        "dst": "models/upscale_models",
        "extensions": [".pth", ".pt"]
    }
}

def copy_models(model_type, dry_run=False):
    """指定されたタイプのモデルをコピー"""
    if model_type not in MODEL_MAPPINGS:
        print(f"Error: Unknown model type '{model_type}'")
        return False
    
    mapping = MODEL_MAPPINGS[model_type]
    src_dir = Path(A1111_PATH) / mapping["src"]
    dst_dir = Path(COMFYUI_PATH) / mapping["dst"]
    
    if not src_dir.exists():
        print(f"Source directory not found: {src_dir}")
        return False
    
    # コピー先ディレクトリを作成
    if not dry_run:
        dst_dir.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    skipped_count = 0
    total_size = 0
    
    print(f"\nCopying {model_type} from:")
    print(f"  {src_dir}")
    print(f"to:")
    print(f"  {dst_dir}")
    print("-" * 60)
    
    # ファイルをコピー
    for file_path in src_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in mapping["extensions"]:
            relative_path = file_path.relative_to(src_dir)
            dst_path = dst_dir / relative_path
            
            # ファイルサイズ
            file_size = file_path.stat().st_size / (1024 * 1024)  # MB
            
            if dst_path.exists():
                print(f"[SKIP] {relative_path} (already exists)")
                skipped_count += 1
            else:
                if dry_run:
                    print(f"[DRY-RUN] {relative_path} ({file_size:.1f} MB)")
                else:
                    # サブディレクトリを作成
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    print(f"[COPY] {relative_path} ({file_size:.1f} MB)")
                    shutil.copy2(file_path, dst_path)
                copied_count += 1
                total_size += file_size
    
    print("-" * 60)
    print(f"Summary: {copied_count} files to copy ({total_size:.1f} MB), {skipped_count} skipped")
    return True

def main():
    """メイン処理"""
    print("A1111 to ComfyUI Model Copy Tool")
    print("=" * 60)
    
    # 引数処理
    if len(sys.argv) < 2:
        print("\nUsage:")
        print(f"  python {sys.argv[0]} <model_type|all> [--dry-run]")
        print(f"\nModel types:")
        for model_type in MODEL_MAPPINGS:
            print(f"  - {model_type}")
        print(f"  - all (copy all model types)")
        print(f"\nOptions:")
        print(f"  --dry-run  Show what would be copied without actually copying")
        return
    
    model_type = sys.argv[1].lower()
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("\n*** DRY RUN MODE - No files will be copied ***")
    
    # パスの確認
    if not Path(A1111_PATH).exists():
        print(f"\nError: A1111 path not found: {A1111_PATH}")
        return
    
    if not Path(COMFYUI_PATH).exists():
        print(f"\nError: ComfyUI path not found: {COMFYUI_PATH}")
        return
    
    # モデルのコピー
    if model_type == "all":
        for mt in MODEL_MAPPINGS:
            copy_models(mt, dry_run)
            print()
    else:
        copy_models(model_type, dry_run)
    
    print("\nDone!")

if __name__ == "__main__":
    main()