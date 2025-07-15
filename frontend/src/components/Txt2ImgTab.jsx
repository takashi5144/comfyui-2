import React, { useState } from 'react'
import { toast } from 'react-toastify'
import PromptInput from './PromptInput'
import GenerationSettings from './GenerationSettings'
import ImageViewer from './ImageViewer'
import GenerateButton from './GenerateButton'
import { generateImage, pollGenerationStatus, getGenerationHistory, getPreviewImageUrl } from '../api/comfyui'

const Txt2ImgTab = ({ models, samplers, schedulers }) => {
  const [settings, setSettings] = useState({
    mode: 'txt2img',
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
  })
  
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedImages, setGeneratedImages] = useState([])
  const [progress, setProgress] = useState(null)

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  const handleGenerate = async () => {
    if (!settings.prompt.trim()) {
      toast.error('プロンプトを入力してください')
      return
    }

    setIsGenerating(true)
    setProgress({ status: 'starting', progress: 0 })

    try {
      console.log('Starting image generation with settings:', settings)
      
      // 画像生成リクエスト
      const generateParams = {
        mode: 'txt2img',
        ...settings
      }
      const result = await generateImage(generateParams)
      console.log('Generation started:', result)
      
      if (result.success) {
        toast.success('画像生成を開始しました')
        
        // 生成状態のポーリング
        const finalStatus = await pollGenerationStatus(
          result.prompt_id,
          (status) => {
            console.log('Generation status update:', status)
            setProgress({
              status: status.status,
              progress: status.progress,
              queuePosition: status.queue_position
            })
          }
        )
        
        if (finalStatus.status === 'completed') {
          // 生成された画像を取得
          const history = await getGenerationHistory(result.prompt_id)
          console.log('Generation history:', history)
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
      console.error('Error details:', {
        message: error.message,
        response: error.response,
        request: error.request
      })
      toast.error(error.message || 'エラーが発生しました')
    } finally {
      setIsGenerating(false)
      setProgress(null)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* 左側：設定パネル */}
      <div className="space-y-6">
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

export default Txt2ImgTab