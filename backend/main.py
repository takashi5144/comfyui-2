"""
ComfyUI A1111-Style Interface - Backend API Server
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import aiohttp
import json
import uuid
import asyncio
import io
from PIL import Image
import base64
from datetime import datetime
import os

from comfyui_bridge import ComfyUIBridge
from workflow_manager import WorkflowManager
from samplers_config import get_sampler_list, get_scheduler_list, get_samplers_by_category, get_schedulers_by_category

# FastAPIアプリケーションの初期化
app = FastAPI(title="ComfyUI A1111-Style API", version="1.0.0")

# CORS設定（開発環境用に寛容な設定）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# ComfyUIブリッジとワークフロー管理の初期化
comfyui_bridge = ComfyUIBridge()
workflow_manager = WorkflowManager()

# リクエストモデル
class GenerateRequest(BaseModel):
    mode: str = "txt2img"  # txt2img, img2img, inpaint
    prompt: str
    negative_prompt: str = ""
    width: int = 512
    height: int = 512
    steps: int = 20
    cfg_scale: float = 7.0
    sampler_name: str = "euler"
    scheduler: str = "normal"
    seed: int = -1
    batch_size: int = 1
    model: str = "v1-5-pruned-emaonly.safetensors"
    vae: Optional[str] = None
    loras: Optional[List[Dict[str, Any]]] = None
    # img2img specific
    init_image: Optional[str] = None
    denoising_strength: float = 0.75
    # inpaint specific
    mask_image: Optional[str] = None

class ModelInfo(BaseModel):
    name: str
    path: str
    type: str

# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "ComfyUI A1111-Style API Server", "status": "running"}

# ヘルスチェックエンドポイント
@app.get("/api/health")
async def health_check():
    """APIサーバーの状態を確認"""
    try:
        # ComfyUIへの接続を確認
        comfyui_status = await comfyui_bridge.check_connection()
        return {
            "status": "healthy",
            "api_version": "1.0.3",
            "comfyui_connected": comfyui_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# 画像生成エンドポイント
@app.post("/api/generate")
async def generate_image(request: GenerateRequest):
    """画像生成のメインエンドポイント"""
    print(f"[DEBUG] Generate request received: mode={request.mode}, model={request.model}")
    print(f"[DEBUG] Request details: {request.dict()}")
    
    try:
        # ワークフローの作成
        if request.mode == "txt2img":
            workflow = workflow_manager.create_txt2img_workflow(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                width=request.width,
                height=request.height,
                steps=request.steps,
                cfg_scale=request.cfg_scale,
                sampler_name=request.sampler_name,
                scheduler=request.scheduler,
                seed=request.seed,
                batch_size=request.batch_size,
                model=request.model,
                vae=request.vae,
                loras=request.loras
            )
        elif request.mode == "img2img":
            workflow = workflow_manager.create_img2img_workflow(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                init_image=request.init_image,
                denoising_strength=request.denoising_strength,
                steps=request.steps,
                cfg_scale=request.cfg_scale,
                sampler_name=request.sampler_name,
                scheduler=request.scheduler,
                seed=request.seed,
                batch_size=request.batch_size,
                model=request.model,
                vae=request.vae,
                loras=request.loras
            )
        elif request.mode == "inpaint":
            workflow = workflow_manager.create_inpaint_workflow(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                init_image=request.init_image,
                mask_image=request.mask_image,
                denoising_strength=request.denoising_strength,
                steps=request.steps,
                cfg_scale=request.cfg_scale,
                sampler_name=request.sampler_name,
                scheduler=request.scheduler,
                seed=request.seed,
                batch_size=request.batch_size,
                model=request.model,
                vae=request.vae,
                loras=request.loras
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unknown mode: {request.mode}")
        
        # ComfyUIに送信
        result = await comfyui_bridge.queue_prompt(workflow)
        
        if result["success"]:
            return {
                "success": True,
                "prompt_id": result["prompt_id"],
                "message": "画像生成を開始しました"
            }
        else:
            print(f"[ERROR] ComfyUI returned error: {result}")
            raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))
            
    except Exception as e:
        print(f"[ERROR] Generate image failed: {str(e)}")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 生成状態確認エンドポイント
@app.get("/api/status/{prompt_id}")
async def get_generation_status(prompt_id: str):
    """生成状態の確認"""
    try:
        status = await comfyui_bridge.get_prompt_status(prompt_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 生成履歴取得エンドポイント
@app.get("/api/history/{prompt_id}")
async def get_generation_history(prompt_id: str):
    """生成履歴と画像の取得"""
    try:
        history = await comfyui_bridge.get_history(prompt_id)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# モデル一覧取得エンドポイント
@app.get("/api/models")
async def get_models():
    """利用可能なモデルの一覧を取得"""
    try:
        models = await comfyui_bridge.get_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# LoRA一覧取得エンドポイント
@app.get("/api/loras")
async def get_loras():
    """利用可能なLoRAの一覧を取得"""
    try:
        loras = await comfyui_bridge.get_loras()
        return {"loras": loras}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# サンプラー一覧取得エンドポイント
@app.get("/api/samplers")
async def get_samplers():
    """利用可能なサンプラーの一覧を取得"""
    return {
        "samplers": get_sampler_list(),
        "samplers_by_category": get_samplers_by_category()
    }

# スケジューラー一覧取得エンドポイント
@app.get("/api/schedulers")
async def get_schedulers():
    """利用可能なスケジューラーの一覧を取得"""
    return {
        "schedulers": get_scheduler_list(),
        "schedulers_by_category": get_schedulers_by_category()
    }

# 画像アップロードエンドポイント
@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    """画像のアップロード（img2img/inpaint用）"""
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Base64エンコード
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "success": True,
            "image": f"data:image/png;base64,{img_base64}",
            "width": image.width,
            "height": image.height
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# プレビュー画像取得エンドポイント
@app.get("/api/preview/{filename}")
async def get_preview_image(filename: str):
    """生成された画像の取得"""
    try:
        image_data = await comfyui_bridge.get_image(filename)
        return StreamingResponse(io.BytesIO(image_data), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image not found")

# WebSocketエンドポイント（リアルタイム更新用）
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # ComfyUIのWebSocketに接続
        async with comfyui_bridge.connect_websocket() as comfyui_ws:
            # メッセージの中継
            async def relay_from_comfyui():
                async for message in comfyui_ws:
                    await websocket.send_text(message)
            
            # 並行してメッセージを処理
            await relay_from_comfyui()
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")

# サーバー起動
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)