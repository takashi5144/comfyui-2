import axios from 'axios'
import { API_CONFIG } from './config.js'

// 本番環境では相対パス、開発環境では設定されたURLを使用
const API_BASE_URL = import.meta.env.MODE === 'production' ? '/api' : `${API_CONFIG.API_URL}/api`

// APIクライアントの作成
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// エラーハンドリング
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    throw error
  }
)

// 画像生成
export const generateImage = async (params) => {
  const response = await apiClient.post('/generate', params)
  return response.data
}

// 生成状態の確認
export const getGenerationStatus = async (promptId) => {
  const response = await apiClient.get(`/status/${promptId}`)
  return response.data
}

// 生成履歴の取得
export const getGenerationHistory = async (promptId) => {
  const response = await apiClient.get(`/history/${promptId}`)
  return response.data
}

// モデル一覧の取得
export const getModels = async () => {
  try {
    const response = await apiClient.get('/models')
    return response.data
  } catch (error) {
    console.error('Failed to fetch models:', error)
    return { models: API_CONFIG.DEFAULT_MODELS }
  }
}

// LoRA一覧の取得
export const getLoras = async () => {
  try {
    const response = await apiClient.get('/loras')
    return response.data
  } catch (error) {
    console.error('Failed to fetch loras:', error)
    return { loras: [] }
  }
}

// サンプラー一覧の取得
export const getSamplers = async () => {
  try {
    const response = await apiClient.get('/samplers')
    return response.data
  } catch (error) {
    console.error('Failed to fetch samplers:', error)
    return { samplers: API_CONFIG.DEFAULT_SAMPLERS }
  }
}

// スケジューラー一覧の取得
export const getSchedulers = async () => {
  try {
    const response = await apiClient.get('/schedulers')
    return response.data
  } catch (error) {
    console.error('Failed to fetch schedulers:', error)
    return { schedulers: API_CONFIG.DEFAULT_SCHEDULERS }
  }
}

// 画像のアップロード
export const uploadImage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await apiClient.post('/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

// プレビュー画像のURL取得
export const getPreviewImageUrl = (filename) => {
  return `${API_BASE_URL}/preview/${filename}`
}

// WebSocket接続の作成
export const createWebSocketConnection = (onMessage) => {
  const wsUrl = import.meta.env.MODE === 'production' 
    ? `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`
    : API_CONFIG.WS_URL + '/ws'
    
  const ws = new WebSocket(wsUrl)
  
  ws.onopen = () => {
    console.log('WebSocket connected')
  }
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    onMessage(data)
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
  }
  
  return ws
}

// 生成状態のポーリング
export const pollGenerationStatus = async (promptId, onUpdate, interval = 1000) => {
  const poll = async () => {
    try {
      const status = await getGenerationStatus(promptId)
      onUpdate(status)
      
      if (status.status === 'completed' || status.status === 'error') {
        return status
      }
      
      await new Promise(resolve => setTimeout(resolve, interval))
      return poll()
    } catch (error) {
      console.error('Polling error:', error)
      throw error
    }
  }
  
  return poll()
}