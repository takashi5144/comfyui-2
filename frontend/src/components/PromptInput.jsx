import React from 'react'

const PromptInput = ({ prompt, negativePrompt, onPromptChange, onNegativePromptChange }) => {
  return (
    <div className="space-y-4">
      <div>
        <label className="label">
          プロンプト
        </label>
        <textarea
          className="textarea-field w-full h-24"
          placeholder="生成したい画像の説明を入力してください..."
          value={prompt}
          onChange={(e) => onPromptChange(e.target.value)}
        />
      </div>
      
      <div>
        <label className="label">
          ネガティブプロンプト
        </label>
        <textarea
          className="textarea-field w-full h-16"
          placeholder="除外したい要素を入力してください..."
          value={negativePrompt}
          onChange={(e) => onNegativePromptChange(e.target.value)}
        />
      </div>
    </div>
  )
}

export default PromptInput