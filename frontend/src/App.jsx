import React, { useState, useEffect } from 'react'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs'
import { ToastContainer, toast } from 'react-toastify'
import 'react-tabs/style/react-tabs.css'

import Txt2ImgTab from './components/Txt2ImgTab'
import Img2ImgTab from './components/Img2ImgTab'
import InpaintTab from './components/InpaintTab'
import Header from './components/Header'
import { getModels, getSamplers, getSchedulers } from './api/comfyui.js'
import { API_CONFIG } from './api/config.js'

function App() {
  const [models, setModels] = useState([])
  const [samplers, setSamplers] = useState([])
  const [schedulers, setSchedulers] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // 初期データの読み込み
    const loadInitialData = async () => {
      try {
        const [modelsData, samplersData, schedulersData] = await Promise.all([
          getModels(),
          getSamplers(),
          getSchedulers()
        ])
        
        // モデルデータの処理
        if (modelsData && modelsData.models) {
          setModels(modelsData.models)
        } else {
          setModels(API_CONFIG.DEFAULT_MODELS)
        }
        
        // サンプラーデータの処理
        if (samplersData && samplersData.samplers) {
          setSamplers(samplersData.samplers)
        } else {
          setSamplers(API_CONFIG.DEFAULT_SAMPLERS)
        }
        
        // スケジューラーデータの処理
        if (schedulersData && schedulersData.schedulers) {
          setSchedulers(schedulersData.schedulers)
        } else {
          setSchedulers(API_CONFIG.DEFAULT_SCHEDULERS)
        }
        setIsLoading(false)
      } catch (error) {
        console.error('Failed to load initial data:', error)
        // エラーが発生してもデフォルト値で続行
        setModels(API_CONFIG.DEFAULT_MODELS)
        setSamplers(API_CONFIG.DEFAULT_SAMPLERS)
        setSchedulers(API_CONFIG.DEFAULT_SCHEDULERS)
        toast.warning('サーバーに接続できません。デフォルト設定を使用します。')
        setIsLoading(false)
      }
    }

    loadInitialData()
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-900">
        <div className="text-white text-xl">読み込み中...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <Header />
      
      <div className="container mx-auto px-4 py-6">
        <Tabs className="bg-gray-800 rounded-lg shadow-xl">
          <TabList className="flex border-b border-gray-700">
            <Tab className="px-6 py-3 cursor-pointer hover:bg-gray-700 transition-colors">
              txt2img
            </Tab>
            <Tab className="px-6 py-3 cursor-pointer hover:bg-gray-700 transition-colors">
              img2img
            </Tab>
            <Tab className="px-6 py-3 cursor-pointer hover:bg-gray-700 transition-colors">
              Inpaint
            </Tab>
          </TabList>

          <div className="p-6">
            <TabPanel>
              <Txt2ImgTab 
                models={models} 
                samplers={samplers} 
                schedulers={schedulers} 
              />
            </TabPanel>
            <TabPanel>
              <Img2ImgTab 
                models={models} 
                samplers={samplers} 
                schedulers={schedulers} 
              />
            </TabPanel>
            <TabPanel>
              <InpaintTab 
                models={models} 
                samplers={samplers} 
                schedulers={schedulers} 
              />
            </TabPanel>
          </div>
        </Tabs>
      </div>

      <ToastContainer 
        position="bottom-right"
        theme="dark"
        autoClose={5000}
      />
    </div>
  )
}

export default App