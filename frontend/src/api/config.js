// API設定
export const API_CONFIG = {
  // 環境変数からAPIのURLを取得、なければデフォルト値を使用
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  WS_URL: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',
  
  // タイムアウト設定
  TIMEOUT: 30000, // 30秒
  
  // リトライ設定
  RETRY_COUNT: 3,
  RETRY_DELAY: 1000, // 1秒
  
  // デフォルト値
  DEFAULT_MODELS: [
    { name: 'v1-5-pruned-emaonly.safetensors', type: 'checkpoint' },
    { name: 'flux_schnell.safetensors', type: 'checkpoint' }
  ],
  
  DEFAULT_SAMPLERS: [
    'euler', 'euler_ancestral', 'euler_cfg_pp',
    'heun', 'heunpp2',
    'dpm_2', 'dpm_2_ancestral', 'dpm_fast',
    'dpmpp_2s_ancestral', 'dpmpp_2m', 'dpmpp_2m_sde',
    'lms', 'ddim', 'ddpm', 'uni_pc'
  ],
  
  DEFAULT_SCHEDULERS: [
    'normal', 'karras', 'exponential',
    'sgm_uniform', 'simple', 'ddim_uniform',
    'beta', 'linear', 'cosine'
  ]
}

// 環境判定
export const isProduction = import.meta.env.MODE === 'production'
export const isDevelopment = import.meta.env.MODE === 'development'