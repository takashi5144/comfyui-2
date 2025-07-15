"""
サンプラーとスケジューラーの設定
ComfyUIで利用可能なすべてのサンプラーとスケジューラーの定義
"""

# ComfyUIで利用可能なサンプラーの完全なリスト
SAMPLERS = {
    # Euler系
    "euler": {
        "name": "Euler",
        "description": "シンプルで高速、安定した結果",
        "category": "基本"
    },
    "euler_cfg_pp": {
        "name": "Euler CFG++", 
        "description": "CFG（Classifier-Free Guidance）を改善したEuler",
        "category": "基本"
    },
    "euler_ancestral": {
        "name": "Euler Ancestral",
        "description": "ノイズを追加してより多様な結果を生成",
        "category": "基本"
    },
    "euler_ancestral_cfg_pp": {
        "name": "Euler Ancestral CFG++",
        "description": "改善されたCFGを持つEuler Ancestral",
        "category": "基本"
    },
    
    # Heun系
    "heun": {
        "name": "Heun",
        "description": "2次の精度を持つサンプラー",
        "category": "基本"
    },
    "heunpp2": {
        "name": "Heun++",
        "description": "改善されたHeunサンプラー",
        "category": "基本"
    },
    
    # DPM系
    "dpm_2": {
        "name": "DPM 2",
        "description": "2次のDPMソルバー",
        "category": "DPM"
    },
    "dpm_2_ancestral": {
        "name": "DPM 2 Ancestral",
        "description": "ノイズ追加版のDPM 2",
        "category": "DPM"
    },
    "dpm_fast": {
        "name": "DPM Fast",
        "description": "高速化されたDPMソルバー",
        "category": "DPM"
    },
    "dpm_adaptive": {
        "name": "DPM Adaptive",
        "description": "適応的なステップサイズを使用",
        "category": "DPM"
    },
    
    # DPM++系
    "dpmpp_2s_ancestral": {
        "name": "DPM++ 2S Ancestral",
        "description": "2次の単一ステップDPM++",
        "category": "DPM++"
    },
    "dpmpp_sde": {
        "name": "DPM++ SDE",
        "description": "確率微分方程式版DPM++",
        "category": "DPM++"
    },
    "dpmpp_sde_gpu": {
        "name": "DPM++ SDE GPU",
        "description": "GPU最適化版DPM++ SDE",
        "category": "DPM++"
    },
    "dpmpp_2m": {
        "name": "DPM++ 2M",
        "description": "2次のマルチステップDPM++",
        "category": "DPM++"
    },
    "dpmpp_2m_sde": {
        "name": "DPM++ 2M SDE",
        "description": "SDE版の2M DPM++",
        "category": "DPM++"
    },
    "dpmpp_2m_sde_gpu": {
        "name": "DPM++ 2M SDE GPU",
        "description": "GPU最適化版DPM++ 2M SDE",
        "category": "DPM++"
    },
    "dpmpp_2m_alt": {
        "name": "DPM++ 2M Alternative",
        "description": "代替実装のDPM++ 2M",
        "category": "DPM++"
    },
    "dpmpp_3m_sde": {
        "name": "DPM++ 3M SDE",
        "description": "3次のマルチステップDPM++ SDE",
        "category": "DPM++"
    },
    "dpmpp_3m_sde_gpu": {
        "name": "DPM++ 3M SDE GPU",
        "description": "GPU最適化版DPM++ 3M SDE",
        "category": "DPM++"
    },
    
    # その他のサンプラー
    "lms": {
        "name": "LMS",
        "description": "Linear Multi-Step method",
        "category": "その他"
    },
    "ddpm": {
        "name": "DDPM",
        "description": "Denoising Diffusion Probabilistic Models",
        "category": "その他"
    },
    "lcm": {
        "name": "LCM",
        "description": "Latent Consistency Models用",
        "category": "特殊"
    },
    "ddim": {
        "name": "DDIM",
        "description": "Denoising Diffusion Implicit Models",
        "category": "その他"
    },
    "plms": {
        "name": "PLMS",
        "description": "Pseudo Linear Multi-Step",
        "category": "その他"
    },
    "uni_pc": {
        "name": "UniPC",
        "description": "Unified Predictor-Corrector",
        "category": "高度"
    },
    "uni_pc_bh2": {
        "name": "UniPC BH2",
        "description": "UniPCのBH2バリアント",
        "category": "高度"
    },
    "restart": {
        "name": "Restart",
        "description": "Restart sampling method",
        "category": "高度"
    },
    "deis": {
        "name": "DEIS",
        "description": "Diffusion Exponential Integrator Sampler",
        "category": "高度"
    },
    "ipndm": {
        "name": "iPNDM",
        "description": "improved Pseudo Numerical methods",
        "category": "高度"
    },
    "ipndm_v": {
        "name": "iPNDM-v",
        "description": "iPNDMのバリアント",
        "category": "高度"
    }
}

# スケジューラーの完全なリスト
SCHEDULERS = {
    # 基本的なスケジューラー
    "normal": {
        "name": "Normal",
        "description": "標準的な線形スケジュール",
        "category": "基本"
    },
    "karras": {
        "name": "Karras",
        "description": "Karrasらによる改善されたスケジュール",
        "category": "基本"
    },
    "exponential": {
        "name": "Exponential",
        "description": "指数関数的なスケジュール",
        "category": "基本"
    },
    
    # 一様分布系
    "sgm_uniform": {
        "name": "SGM Uniform",
        "description": "Stable Diffusion XL用の一様分布",
        "category": "一様分布"
    },
    "simple": {
        "name": "Simple",
        "description": "シンプルな線形スケジュール",
        "category": "基本"
    },
    "ddim_uniform": {
        "name": "DDIM Uniform",
        "description": "DDIM用の一様分布スケジュール",
        "category": "一様分布"
    },
    
    # 追加のスケジューラー
    "beta": {
        "name": "Beta",
        "description": "ベータ分布ベースのスケジュール",
        "category": "高度"
    },
    "linear": {
        "name": "Linear",
        "description": "線形スケジュール",
        "category": "基本"
    },
    "sqrt": {
        "name": "Square Root",
        "description": "平方根スケジュール",
        "category": "高度"
    },
    "cosine": {
        "name": "Cosine",
        "description": "コサイン関数ベースのスケジュール",
        "category": "高度"
    },
    
    # Align Your Steps
    "ays_sd15": {
        "name": "AYS SD1.5",
        "description": "SD1.5用のAlign Your Steps",
        "category": "AYS"
    },
    "ays_sdxl": {
        "name": "AYS SDXL",
        "description": "SDXL用のAlign Your Steps",
        "category": "AYS"
    },
    "ays_sde_sd15": {
        "name": "AYS SDE SD1.5",
        "description": "SD1.5用のAYS SDE版",
        "category": "AYS"
    },
    "ays_sde_sdxl": {
        "name": "AYS SDE SDXL",
        "description": "SDXL用のAYS SDE版",
        "category": "AYS"
    },
    "ays_svd": {
        "name": "AYS SVD",
        "description": "Stable Video Diffusion用のAYS",
        "category": "AYS"
    },
    
    # その他の高度なスケジューラー
    "vp": {
        "name": "VP",
        "description": "Variance Preserving",
        "category": "高度"
    },
    "lcm": {
        "name": "LCM",
        "description": "Latent Consistency Model用",
        "category": "特殊"
    },
    "gits": {
        "name": "GITS",
        "description": "Generalized Implicit Sampler",
        "category": "高度"
    },
    "kl_optimal": {
        "name": "KL Optimal",
        "description": "KLダイバージェンス最適化",
        "category": "高度"
    },
    "align_your_steps": {
        "name": "Align Your Steps",
        "description": "汎用AYSスケジューラー",
        "category": "AYS"
    }
}

def get_sampler_list():
    """サンプラー名のリストを取得"""
    return list(SAMPLERS.keys())

def get_scheduler_list():
    """スケジューラー名のリストを取得"""
    return list(SCHEDULERS.keys())

def get_sampler_info(sampler_name):
    """サンプラーの詳細情報を取得"""
    return SAMPLERS.get(sampler_name, {})

def get_scheduler_info(scheduler_name):
    """スケジューラーの詳細情報を取得"""
    return SCHEDULERS.get(scheduler_name, {})

def get_samplers_by_category():
    """カテゴリー別にサンプラーを整理"""
    categories = {}
    for key, info in SAMPLERS.items():
        category = info.get("category", "その他")
        if category not in categories:
            categories[category] = []
        categories[category].append({
            "value": key,
            "name": info["name"],
            "description": info["description"]
        })
    return categories

def get_schedulers_by_category():
    """カテゴリー別にスケジューラーを整理"""
    categories = {}
    for key, info in SCHEDULERS.items():
        category = info.get("category", "その他")
        if category not in categories:
            categories[category] = []
        categories[category].append({
            "value": key,
            "name": info["name"],
            "description": info["description"]
        })
    return categories