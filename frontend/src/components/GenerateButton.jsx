import React from 'react'

const GenerateButton = ({ onClick, isGenerating, progress }) => {
  const getButtonText = () => {
    if (!isGenerating) return '生成'
    
    if (progress?.status === 'pending') {
      return `キュー位置: ${progress.queuePosition}`
    }
    
    if (progress?.status === 'running') {
      return `生成中...`
    }
    
    return '処理中...'
  }
  
  const getProgressBar = () => {
    if (!isGenerating || !progress) return null
    
    if (progress.status === 'running' && progress.progress) {
      const percentage = Math.round(progress.progress * 100)
      return (
        <div className="mt-2">
          <div className="bg-gray-700 rounded-full h-2">
            <div 
              className="bg-orange-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${percentage}%` }}
            />
          </div>
          <p className="text-xs text-gray-400 mt-1 text-center">{percentage}%</p>
        </div>
      )
    }
    
    return null
  }
  
  return (
    <div className="space-y-2">
      <button
        className={`btn-primary w-full text-lg py-3 ${isGenerating ? 'opacity-50 cursor-not-allowed' : ''}`}
        onClick={onClick}
        disabled={isGenerating}
      >
        {getButtonText()}
      </button>
      {getProgressBar()}
      {isGenerating && (
        <button
          className="btn-secondary w-full"
          onClick={() => {/* TODO: 中断機能の実装 */}}
        >
          中断
        </button>
      )}
    </div>
  )
}

export default GenerateButton