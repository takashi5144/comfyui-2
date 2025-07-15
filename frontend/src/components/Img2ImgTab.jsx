import React, { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'react-toastify'
import PromptInput from './PromptInput'
import GenerationSettings from './GenerationSettings'
import ImageViewer from './ImageViewer'
import GenerateButton from './GenerateButton'
import { generateImage, uploadImage, pollGenerationStatus, getGenerationHistory, getPreviewImageUrl } from '../api/comfyui'

const Img2ImgTab = ({ models, samplers, schedulers }) => {
  const [settings, setSettings] = useState({
    mode: 'img2img',
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
    denoising_strength: 0.75,
    init_image: null,
  })
  
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedImages, setGeneratedImages] = useState([])
  const [progress, setProgress] = useState(null)
  const [uploadedImage, setUploadedImage] = useState(null)

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

  const handleGenerate = async () => {
    if (!settings.prompt.trim()) {
      toast.error('プロンプトを入力してください')
      return
    }
    
    if (!settings.init_image) {
      toast.error('画像をアップロードしてください')
      return
    }

    setIsGenerating(true)
    setProgress({ status: 'starting', progress: 0 })

    try {
      const result = await generateImage(settings)
      
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
        {/* 画像アップロードエリア */}
        <div className="card">
          <h3 className="text-lg font-semibold text-orange-400 mb-4">入力画像</h3>
          <div
            {...getRootProps()}
            className={`image-preview h-64 cursor-pointer ${
              isDragActive ? 'border-orange-500' : ''
            }`}
          >
            <input {...getInputProps()} />
            {uploadedImage ? (
              <img
                src={uploadedImage}
                alt="Uploaded"
                className="w-full h-full object-contain"
              />
            ) : (
              <div className="h-full flex items-center justify-center">
                <p className="text-gray-500">
                  {isDragActive
                    ? '画像をドロップしてください'
                    : 'クリックまたはドラッグ&ドロップで画像をアップロード'}
                </p>
              </div>
            )}
          </div>
        </div>

        <PromptInput
          prompt={settings.prompt}
          negativePrompt={settings.negative_prompt}
          onPromptChange={(value) => handleSettingChange('prompt', value)}
          onNegativePromptChange={(value) => handleSettingChange('negative_prompt', value)}
        />
        
        {/* Denoising Strength */}
        <div className="card">
          <label className="label">Denoising Strength: {settings.denoising_strength.toFixed(2)}</label>
          <div className="slider-container">
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={settings.denoising_strength}
              onChange={(e) => handleSettingChange('denoising_strength', parseFloat(e.target.value))}
              className="flex-1"
            />
            <input
              type="number"
              className="input-field w-20"
              value={settings.denoising_strength}
              onChange={(e) => handleSettingChange('denoising_strength', parseFloat(e.target.value))}
              min="0"
              max="1"
              step="0.05"
            />
          </div>
        </div>
        
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

export default Img2ImgTab