import React, { useState } from 'react'

const ImageViewer = ({ images, isGenerating, progress }) => {
  const [selectedImage, setSelectedImage] = useState(null)
  
  if (isGenerating && images.length === 0) {
    return (
      <div className="image-preview h-96 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-gray-400">
            {progress?.status === 'pending' ? 'キューで待機中...' : '画像を生成中...'}
          </p>
        </div>
      </div>
    )
  }
  
  if (images.length === 0) {
    return (
      <div className="image-preview h-96 flex items-center justify-center">
        <p className="text-gray-500">
          生成された画像がここに表示されます
        </p>
      </div>
    )
  }
  
  return (
    <div className="space-y-4">
      {/* メイン画像表示 */}
      <div className="bg-gray-900 rounded-lg p-4">
        <img
          src={selectedImage || images[0].url}
          alt="Generated"
          className="w-full h-auto rounded-lg cursor-pointer"
          onClick={() => {
            // TODO: フルスクリーン表示機能
          }}
        />
      </div>
      
      {/* サムネイル一覧 */}
      {images.length > 1 && (
        <div className="grid grid-cols-4 gap-2">
          {images.map((image, index) => (
            <div
              key={index}
              className={`cursor-pointer rounded border-2 ${
                (selectedImage || images[0].url) === image.url
                  ? 'border-orange-500'
                  : 'border-transparent'
              }`}
              onClick={() => setSelectedImage(image.url)}
            >
              <img
                src={image.url}
                alt={`Generated ${index + 1}`}
                className="w-full h-auto rounded"
              />
            </div>
          ))}
        </div>
      )}
      
      {/* 画像情報と操作ボタン */}
      <div className="flex justify-between items-center mt-4">
        <div className="text-sm text-gray-400">
          {images.length} 枚の画像
        </div>
        <div className="space-x-2">
          <button className="btn-secondary text-sm">
            💾 保存
          </button>
          <button className="btn-secondary text-sm">
            📋 設定をコピー
          </button>
        </div>
      </div>
    </div>
  )
}

export default ImageViewer