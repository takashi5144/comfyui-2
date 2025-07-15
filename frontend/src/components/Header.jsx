import React from 'react'

const Header = () => {
  return (
    <header className="bg-gray-800 border-b border-gray-700 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-orange-500">
            ComfyUI A1111-Style Interface
          </h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-400">
              ComfyUIバックエンド使用
            </span>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-300">接続済み</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header