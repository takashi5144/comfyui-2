"""
ComfyUI Bridge - ComfyUIとの通信を管理
"""

import aiohttp
import json
import asyncio
from typing import Dict, Any, Optional, List
import websockets
import uuid
import os
from datetime import datetime

class ComfyUIBridge:
    def __init__(self, comfyui_url: str = "http://127.0.0.1:8188"):
        self.comfyui_url = comfyui_url
        self.client_id = str(uuid.uuid4())
        
    async def queue_prompt(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """ワークフローをComfyUIのキューに送信"""
        try:
            prompt = {"prompt": workflow, "client_id": self.client_id}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.comfyui_url}/prompt",
                    json=prompt
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "success": True,
                            "prompt_id": result.get("prompt_id"),
                            "number": result.get("number", 0)
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"ComfyUI returned status {response.status}: {error_text}"
                        }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to connect to ComfyUI: {str(e)}"
            }
    
    async def get_prompt_status(self, prompt_id: str) -> Dict[str, Any]:
        """プロンプトの実行状態を取得"""
        try:
            async with aiohttp.ClientSession() as session:
                # キューの状態を確認
                async with session.get(f"{self.comfyui_url}/queue") as response:
                    if response.status == 200:
                        queue_data = await response.json()
                        
                        # 実行中のプロンプトを確認
                        running = queue_data.get("queue_running", [])
                        for item in running:
                            if item[1] == prompt_id:
                                return {
                                    "status": "running",
                                    "queue_position": 0,
                                    "progress": item[2] if len(item) > 2 else None
                                }
                        
                        # 待機中のプロンプトを確認
                        pending = queue_data.get("queue_pending", [])
                        for i, item in enumerate(pending):
                            if item[1] == prompt_id:
                                return {
                                    "status": "pending",
                                    "queue_position": i + 1,
                                    "progress": None
                                }
                        
                        # 履歴を確認（完了済み）
                        history = await self.get_history(prompt_id)
                        if history.get("outputs"):
                            return {
                                "status": "completed",
                                "queue_position": 0,
                                "progress": None,
                                "outputs": history["outputs"]
                            }
                        
                        return {
                            "status": "not_found",
                            "queue_position": -1,
                            "progress": None
                        }
                    else:
                        return {
                            "status": "error",
                            "error": f"Failed to get queue status: {response.status}"
                        }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """プロンプトの実行履歴を取得"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.comfyui_url}/history/{prompt_id}") as response:
                    if response.status == 200:
                        history = await response.json()
                        
                        if prompt_id in history:
                            prompt_history = history[prompt_id]
                            outputs = prompt_history.get("outputs", {})
                            
                            # 画像出力を整理
                            images = []
                            for node_id, node_output in outputs.items():
                                if "images" in node_output:
                                    for image in node_output["images"]:
                                        images.append({
                                            "filename": image["filename"],
                                            "subfolder": image.get("subfolder", ""),
                                            "type": image.get("type", "output"),
                                            "node_id": node_id
                                        })
                            
                            return {
                                "prompt_id": prompt_id,
                                "outputs": images,
                                "status": prompt_history.get("status", {}),
                                "completed_at": datetime.now().isoformat()
                            }
                        else:
                            return {
                                "prompt_id": prompt_id,
                                "outputs": [],
                                "status": "not_found"
                            }
                    else:
                        return {
                            "error": f"Failed to get history: {response.status}"
                        }
        except Exception as e:
            return {
                "error": str(e)
            }
    
    async def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """ComfyUIから画像を取得"""
        try:
            params = {
                "filename": filename,
                "subfolder": subfolder,
                "type": folder_type
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.comfyui_url}/view",
                    params=params
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        raise Exception(f"Failed to get image: {response.status}")
        except Exception as e:
            raise Exception(f"Failed to get image: {str(e)}")
    
    async def get_models(self) -> List[Dict[str, str]]:
        """利用可能なモデルの一覧を取得"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.comfyui_url}/object_info") as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # CheckpointLoaderSimpleノードの情報から取得
                        checkpoint_loader = data.get("CheckpointLoaderSimple", {})
                        input_info = checkpoint_loader.get("input", {}).get("required", {})
                        ckpt_names = input_info.get("ckpt_name", [[]])[0]
                        
                        models = []
                        for model_name in ckpt_names:
                            models.append({
                                "name": model_name,
                                "type": "checkpoint"
                            })
                        
                        return models
                    else:
                        return []
        except Exception as e:
            print(f"Failed to get models: {e}")
            return []
    
    async def get_loras(self) -> List[Dict[str, str]]:
        """利用可能なLoRAの一覧を取得"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.comfyui_url}/object_info") as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # LoraLoaderノードの情報から取得
                        lora_loader = data.get("LoraLoader", {})
                        input_info = lora_loader.get("input", {}).get("required", {})
                        lora_names = input_info.get("lora_name", [[]])[0]
                        
                        loras = []
                        for lora_name in lora_names:
                            loras.append({
                                "name": lora_name,
                                "type": "lora"
                            })
                        
                        return loras
                    else:
                        return []
        except Exception as e:
            print(f"Failed to get LoRAs: {e}")
            return []
    
    async def interrupt(self) -> bool:
        """現在の生成を中断"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.comfyui_url}/interrupt") as response:
                    return response.status == 200
        except Exception as e:
            print(f"Failed to interrupt: {e}")
            return False
    
    async def clear_queue(self) -> bool:
        """キューをクリア"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{self.comfyui_url}/queue") as response:
                    return response.status == 200
        except Exception as e:
            print(f"Failed to clear queue: {e}")
            return False
    
    async def connect_websocket(self):
        """ComfyUIのWebSocketに接続"""
        ws_url = self.comfyui_url.replace("http://", "ws://").replace("https://", "wss://")
        return await websockets.connect(f"{ws_url}/ws?clientId={self.client_id}")