"""
Workflow Manager - ComfyUIワークフローの作成と管理
"""

import json
import random
from typing import Dict, Any, List, Optional
import uuid

class WorkflowManager:
    def __init__(self):
        self.node_counter = 0
        
    def _next_node_id(self) -> str:
        """次のノードIDを生成"""
        self.node_counter += 1
        return str(self.node_counter)
    
    def _reset_counter(self):
        """ノードカウンターをリセット"""
        self.node_counter = 0
    
    def create_txt2img_workflow(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        cfg_scale: float = 7.0,
        sampler_name: str = "euler",
        scheduler: str = "normal",
        seed: int = -1,
        batch_size: int = 1,
        model: str = "v1-5-pruned-emaonly.safetensors",
        vae: Optional[str] = None,
        loras: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Text2Image用のワークフローを作成"""
        self._reset_counter()
        workflow = {}
        
        # シードの設定（-1の場合はランダム）
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        
        # チェックポイントローダー
        checkpoint_loader_id = self._next_node_id()
        workflow[checkpoint_loader_id] = {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": model
            }
        }
        
        model_output = [checkpoint_loader_id, 0]
        clip_output = [checkpoint_loader_id, 1]
        vae_output = [checkpoint_loader_id, 2]
        
        # VAEローダー（指定された場合）
        if vae:
            vae_loader_id = self._next_node_id()
            workflow[vae_loader_id] = {
                "class_type": "VAELoader",
                "inputs": {
                    "vae_name": vae
                }
            }
            vae_output = [vae_loader_id, 0]
        
        # LoRAの適用
        if loras:
            for lora in loras:
                lora_loader_id = self._next_node_id()
                workflow[lora_loader_id] = {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": lora["name"],
                        "strength_model": lora.get("strength", 1.0),
                        "strength_clip": lora.get("strength", 1.0),
                        "model": model_output,
                        "clip": clip_output
                    }
                }
                model_output = [lora_loader_id, 0]
                clip_output = [lora_loader_id, 1]
        
        # ポジティブプロンプト
        positive_prompt_id = self._next_node_id()
        workflow[positive_prompt_id] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt,
                "clip": clip_output
            }
        }
        
        # ネガティブプロンプト
        negative_prompt_id = self._next_node_id()
        workflow[negative_prompt_id] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": clip_output
            }
        }
        
        # 空のLatent画像
        empty_latent_id = self._next_node_id()
        workflow[empty_latent_id] = {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": batch_size
            }
        }
        
        # KSampler
        ksampler_id = self._next_node_id()
        workflow[ksampler_id] = {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg_scale,
                "sampler_name": sampler_name,
                "scheduler": scheduler,
                "denoise": 1.0,
                "model": model_output,
                "positive": [positive_prompt_id, 0],
                "negative": [negative_prompt_id, 0],
                "latent_image": [empty_latent_id, 0]
            }
        }
        
        # VAEデコード
        vae_decode_id = self._next_node_id()
        workflow[vae_decode_id] = {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": [ksampler_id, 0],
                "vae": vae_output
            }
        }
        
        # 画像保存
        save_image_id = self._next_node_id()
        workflow[save_image_id] = {
            "class_type": "SaveImage",
            "inputs": {
                "images": [vae_decode_id, 0],
                "filename_prefix": "ComfyUI_A1111"
            }
        }
        
        return workflow
    
    def create_img2img_workflow(
        self,
        prompt: str,
        negative_prompt: str = "",
        init_image: str = "",
        denoising_strength: float = 0.75,
        steps: int = 20,
        cfg_scale: float = 7.0,
        sampler_name: str = "euler",
        scheduler: str = "normal",
        seed: int = -1,
        batch_size: int = 1,
        model: str = "v1-5-pruned-emaonly.safetensors",
        vae: Optional[str] = None,
        loras: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Img2Img用のワークフローを作成"""
        self._reset_counter()
        workflow = {}
        
        # シードの設定
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        
        # チェックポイントローダー
        checkpoint_loader_id = self._next_node_id()
        workflow[checkpoint_loader_id] = {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": model
            }
        }
        
        model_output = [checkpoint_loader_id, 0]
        clip_output = [checkpoint_loader_id, 1]
        vae_output = [checkpoint_loader_id, 2]
        
        # 画像ローダー
        load_image_id = self._next_node_id()
        workflow[load_image_id] = {
            "class_type": "LoadImage",
            "inputs": {
                "image": init_image,
                "upload": "image"
            }
        }
        
        # VAEエンコード（画像をLatentに変換）
        vae_encode_id = self._next_node_id()
        workflow[vae_encode_id] = {
            "class_type": "VAEEncode",
            "inputs": {
                "pixels": [load_image_id, 0],
                "vae": vae_output
            }
        }
        
        # LoRAの適用
        if loras:
            for lora in loras:
                lora_loader_id = self._next_node_id()
                workflow[lora_loader_id] = {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": lora["name"],
                        "strength_model": lora.get("strength", 1.0),
                        "strength_clip": lora.get("strength", 1.0),
                        "model": model_output,
                        "clip": clip_output
                    }
                }
                model_output = [lora_loader_id, 0]
                clip_output = [lora_loader_id, 1]
        
        # ポジティブプロンプト
        positive_prompt_id = self._next_node_id()
        workflow[positive_prompt_id] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt,
                "clip": clip_output
            }
        }
        
        # ネガティブプロンプト
        negative_prompt_id = self._next_node_id()
        workflow[negative_prompt_id] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": clip_output
            }
        }
        
        # KSampler
        ksampler_id = self._next_node_id()
        workflow[ksampler_id] = {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg_scale,
                "sampler_name": sampler_name,
                "scheduler": scheduler,
                "denoise": denoising_strength,
                "model": model_output,
                "positive": [positive_prompt_id, 0],
                "negative": [negative_prompt_id, 0],
                "latent_image": [vae_encode_id, 0]
            }
        }
        
        # VAEデコード
        vae_decode_id = self._next_node_id()
        workflow[vae_decode_id] = {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": [ksampler_id, 0],
                "vae": vae_output
            }
        }
        
        # 画像保存
        save_image_id = self._next_node_id()
        workflow[save_image_id] = {
            "class_type": "SaveImage",
            "inputs": {
                "images": [vae_decode_id, 0],
                "filename_prefix": "ComfyUI_A1111_img2img"
            }
        }
        
        return workflow
    
    def create_inpaint_workflow(
        self,
        prompt: str,
        negative_prompt: str = "",
        init_image: str = "",
        mask_image: str = "",
        denoising_strength: float = 1.0,
        steps: int = 20,
        cfg_scale: float = 7.0,
        sampler_name: str = "euler",
        scheduler: str = "normal",
        seed: int = -1,
        batch_size: int = 1,
        model: str = "v1-5-pruned-emaonly.safetensors",
        vae: Optional[str] = None,
        loras: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Inpainting用のワークフローを作成"""
        self._reset_counter()
        workflow = {}
        
        # シードの設定
        if seed == -1:
            seed = random.randint(0, 0xffffffffffffffff)
        
        # チェックポイントローダー
        checkpoint_loader_id = self._next_node_id()
        workflow[checkpoint_loader_id] = {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": model
            }
        }
        
        model_output = [checkpoint_loader_id, 0]
        clip_output = [checkpoint_loader_id, 1]
        vae_output = [checkpoint_loader_id, 2]
        
        # 画像ローダー
        load_image_id = self._next_node_id()
        workflow[load_image_id] = {
            "class_type": "LoadImage",
            "inputs": {
                "image": init_image,
                "upload": "image"
            }
        }
        
        # マスクローダー
        load_mask_id = self._next_node_id()
        workflow[load_mask_id] = {
            "class_type": "LoadImageMask",
            "inputs": {
                "image": mask_image,
                "channel": "red",
                "upload": "image"
            }
        }
        
        # VAEエンコード（マスク付き）
        vae_encode_inpaint_id = self._next_node_id()
        workflow[vae_encode_inpaint_id] = {
            "class_type": "VAEEncodeForInpaint",
            "inputs": {
                "pixels": [load_image_id, 0],
                "vae": vae_output,
                "mask": [load_mask_id, 0],
                "grow_mask_by": 6
            }
        }
        
        # LoRAの適用
        if loras:
            for lora in loras:
                lora_loader_id = self._next_node_id()
                workflow[lora_loader_id] = {
                    "class_type": "LoraLoader",
                    "inputs": {
                        "lora_name": lora["name"],
                        "strength_model": lora.get("strength", 1.0),
                        "strength_clip": lora.get("strength", 1.0),
                        "model": model_output,
                        "clip": clip_output
                    }
                }
                model_output = [lora_loader_id, 0]
                clip_output = [lora_loader_id, 1]
        
        # ポジティブプロンプト
        positive_prompt_id = self._next_node_id()
        workflow[positive_prompt_id] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt,
                "clip": clip_output
            }
        }
        
        # ネガティブプロンプト
        negative_prompt_id = self._next_node_id()
        workflow[negative_prompt_id] = {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": clip_output
            }
        }
        
        # KSampler
        ksampler_id = self._next_node_id()
        workflow[ksampler_id] = {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg_scale,
                "sampler_name": sampler_name,
                "scheduler": scheduler,
                "denoise": denoising_strength,
                "model": model_output,
                "positive": [positive_prompt_id, 0],
                "negative": [negative_prompt_id, 0],
                "latent_image": [vae_encode_inpaint_id, 0]
            }
        }
        
        # VAEデコード
        vae_decode_id = self._next_node_id()
        workflow[vae_decode_id] = {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": [ksampler_id, 0],
                "vae": vae_output
            }
        }
        
        # 画像保存
        save_image_id = self._next_node_id()
        workflow[save_image_id] = {
            "class_type": "SaveImage",
            "inputs": {
                "images": [vae_decode_id, 0],
                "filename_prefix": "ComfyUI_A1111_inpaint"
            }
        }
        
        return workflow