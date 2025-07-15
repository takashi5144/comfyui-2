import React, { useState, useRef, useEffect } from 'react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'react-toastify'
import PromptInput from './PromptInput'
import GenerationSettings from './GenerationSettings'
import ImageViewer from './ImageViewer'
import GenerateButton from './GenerateButton'
import { generateImage, uploadImage, pollGenerationStatus, getGenerationHistory, getPreviewImageUrl } from '../api/comfyui'

const InpaintTab = ({ models, samplers, schedulers }) => {
  const canvasRef = useRef(null)
  const [settings, setSettings] = useState({
    mode: 'inpaint',
    prompt: '',
    negative_prompt: '',
    width: 512,
    height: 512,
    steps: 20,
    cfg_scale: 7.0,
    sampler_name: 'euler',
    scheduler: 'normal',
    seed: -1,
    batch_size: 1,
    model: models[0]?.name || '',
    denoising_strength: 1.0,
    init_image: null,
    mask_image: null,
  })
  
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedImages, setGeneratedImages] = useState([])
  const [progress, setProgress] = useState(null)
  const [uploadedImage, setUploadedImage] = useState(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [brushSize, setBrushSize] = useState(20)
  const [isErasing, setIsErasing] = useState(false)

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0]
      
      try {
        const result = await uploadImage(file)
        if (result.success) {
          setUploadedImage(result.image)
          setSettings(prev => ({
            ...prev,
            init_image: result.image,
            width: result.width,
            height: result.height
          }))
          
          // キャンバスをリセット
          const canvas = canvasRef.current
          if (canvas) {
            const ctx = canvas.getContext('2d')
            canvas.width = result.width
            canvas.height = result.height
            ctx.clearRect(0, 0, canvas.width, canvas.height)
          }
          
          toast.success('画像をアップロードしました')
        }
      } catch (error) {
        toast.error('画像のアップロードに失敗しました')
      }
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.webp']
    },
    maxFiles: 1
  })

  // マウスイベントハンドラー
  const startDrawing = (e) => {
    if (!canvasRef.current) return
    setIsDrawing(true)
    draw(e)
  }

  const stopDrawing = () => {
    setIsDrawing(false)
  }

  const draw = (e) => {
    if (!isDrawing || !canvasRef.current) return
    
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    
    ctx.globalCompositeOperation = isErasing ? 'destination-out' : 'source-over'
    ctx.fillStyle = 'rgba(255, 0, 0, 0.5)'
    ctx.beginPath()
    ctx.arc(x, y, brushSize / 2, 0, 2 * Math.PI)
    ctx.fill()
  }

  const clearMask = () => {
    const canvas = canvasRef.current
    if (canvas) {
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  }

  const getMaskImage = () => {
    const canvas = canvasRef.current
    if (canvas) {
      return canvas.toDataURL('image/png')
    }
    return null
  }

  const handleGenerate = async () => {
    if (!settings.prompt.trim()) {
      toast.error('プロンプトを入力してください')
      return
    }
    
    if (!settings.init_image) {
      toast.error('画像をアップロードしてください')
      return
    }
    
    const maskImage = getMaskImage()
    if (!maskImage) {
      toast.error('マスクを描画してください')
      return
    }

    setIsGenerating(true)
    setProgress({ status: 'starting', progress: 0 })

    try {
      const result = await generateImage({
        ...settings,
        mask_image: maskImage
      })
      
      if (result.success) {
        toast.success('画像生成を開始しました')
        
        const finalStatus = await pollGenerationStatus(
          result.prompt_id,
          (status) => {
            setProgress({
              status: status.status,
              progress: status.progress,
              queuePosition: status.queue_position
            })
          }
        )
        
        if (finalStatus.status === 'completed') {
          const history = await getGenerationHistory(result.prompt_id)
          const images = history.outputs.map(output => ({
            url: getPreviewImageUrl(output.filename),
            filename: output.filename,
            ...output
          }))
          
          setGeneratedImages(images)
          toast.success('画像生成が完了しました')
        } else {
          toast.error('画像生成に失敗しました')
        }
      } else {
        toast.error(result.error || '画像生成に失敗しました')
      }
    } catch (error) {
      console.error('Generation error:', error)
      toast.error('エラーが発生しました: ' + error.message)
    } finally {
      setIsGenerating(false)
      setProgress(null)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* 左側：設定パネル */}
      <div className="space-y-6">
        {/* 画像とマスクエディタ */}
        <div className="card">
          <h3 className="text-lg font-semibold text-orange-400 mb-4">入力画像とマスク</h3>
          
          {!uploadedImage ? (
            <div
              {...getRootProps()}
              className={`image-preview h-64 cursor-pointer ${
                isDragActive ? 'border-orange-500' : ''
              }`}
            >
              <input {...getInputProps()} />
              <div className="h-full flex items-center justify-center">
                <p className="text-gray-500">
                  {isDragActive
                    ? '画像をドロップしてください'
                    : 'クリックまたはドラッグ&ドロップで画像をアップロード'}
                </p>
              </div>
            </div>
          ) : (
            <div className="relative">
              <img
                src={uploadedImage}
                alt="Uploaded"
                className="w-full h-auto"
              />
              <canvas
                ref={canvasRef}
                className="absolute top-0 left-0 cursor-crosshair"
                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={stopDrawing}
                onMouseLeave={stopDrawing}
                style={{ width: '100%', height: '100%' }}
              />
            </div>
          )}
          
          {uploadedImage && (
            <div className="mt-4 space-y-2">
              <div className="flex justify-between items-center">
                <div className="flex space-x-2">
                  <button
                    className={`btn-secondary ${!isErasing ? 'bg-orange-600' : ''}`}
                    onClick={() => setIsErasing(false)}
                  >
                    🖌️ 描画
                  </button>
                  <button
                    className={`btn-secondary ${isErasing ? 'bg-orange-600' : ''}`}
                    onClick={() => setIsErasing(true)}
                  >
                    🧹 消去
                  </button>
                  <button
                    className="btn-secondary"
                    onClick={clearMask}
                  >
                    🗑️ クリア
                  </button>
                </div>
              </div>
              
              <div>
                <label className="label">ブラシサイズ: {brushSize}</label>
                <input
                  type="range"
                  min="5"
                  max="100"
                  value={brushSize}
                  onChange={(e) => setBrushSize(parseInt(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          )}
        </div>

        <PromptInput
          prompt={settings.prompt}
          negativePrompt={settings.negative_prompt}
          onPromptChange={(value) => handleSettingChange('prompt', value)}
          onNegativePromptChange={(value) => handleSettingChange('negative_prompt', value)}
        />
        
        <GenerationSettings
          settings={settings}
          models={models}
          samplers={samplers}
          schedulers={schedulers}
          onChange={handleSettingChange}
        />
        
        <GenerateButton
          onClick={handleGenerate}
          isGenerating={isGenerating}
          progress={progress}
        />
      </div>
      
      {/* 右側：画像表示エリア */}
      <div>
        <ImageViewer
          images={generatedImages}
          isGenerating={isGenerating}
          progress={progress}
        />
      </div>
    </div>
  )
}

export default InpaintTab