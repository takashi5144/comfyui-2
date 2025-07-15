import React from 'react'

const GenerationSettings = ({ settings, models, samplers, schedulers, onChange }) => {
  return (
    <div className="card space-y-4">
      <h3 className="text-lg font-semibold text-orange-400 mb-4">生成設定</h3>
      
      {/* モデル選択 */}
      <div>
        <label className="label">モデル</label>
        <select
          className="select-field w-full"
          value={settings.model}
          onChange={(e) => onChange('model', e.target.value)}
        >
          {models.map((model) => (
            <option key={model.name} value={model.name}>
              {model.name}
            </option>
          ))}
        </select>
      </div>
      
      {/* 画像サイズ */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">幅</label>
          <input
            type="number"
            className="input-field w-full"
            value={settings.width}
            onChange={(e) => onChange('width', parseInt(e.target.value))}
            min="64"
            max="2048"
            step="64"
          />
        </div>
        <div>
          <label className="label">高さ</label>
          <input
            type="number"
            className="input-field w-full"
            value={settings.height}
            onChange={(e) => onChange('height', parseInt(e.target.value))}
            min="64"
            max="2048"
            step="64"
          />
        </div>
      </div>
      
      {/* ステップ数 */}
      <div>
        <label className="label">ステップ数: {settings.steps}</label>
        <div className="slider-container">
          <input
            type="range"
            min="1"
            max="150"
            value={settings.steps}
            onChange={(e) => onChange('steps', parseInt(e.target.value))}
            className="flex-1"
          />
          <input
            type="number"
            className="input-field w-20"
            value={settings.steps}
            onChange={(e) => onChange('steps', parseInt(e.target.value))}
            min="1"
            max="150"
          />
        </div>
      </div>
      
      {/* CFGスケール */}
      <div>
        <label className="label">CFGスケール: {settings.cfg_scale.toFixed(1)}</label>
        <div className="slider-container">
          <input
            type="range"
            min="1"
            max="30"
            step="0.5"
            value={settings.cfg_scale}
            onChange={(e) => onChange('cfg_scale', parseFloat(e.target.value))}
            className="flex-1"
          />
          <input
            type="number"
            className="input-field w-20"
            value={settings.cfg_scale}
            onChange={(e) => onChange('cfg_scale', parseFloat(e.target.value))}
            min="1"
            max="30"
            step="0.5"
          />
        </div>
      </div>
      
      {/* サンプラー */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="label">サンプラー</label>
          <select
            className="select-field w-full"
            value={settings.sampler_name}
            onChange={(e) => onChange('sampler_name', e.target.value)}
          >
            {samplers.map((sampler) => (
              <option key={sampler} value={sampler}>
                {sampler}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="label">スケジューラー</label>
          <select
            className="select-field w-full"
            value={settings.scheduler}
            onChange={(e) => onChange('scheduler', e.target.value)}
          >
            {schedulers.map((scheduler) => (
              <option key={scheduler} value={scheduler}>
                {scheduler}
              </option>
            ))}
          </select>
        </div>
      </div>
      
      {/* シード */}
      <div>
        <label className="label">シード</label>
        <div className="flex space-x-2">
          <input
            type="number"
            className="input-field flex-1"
            value={settings.seed}
            onChange={(e) => onChange('seed', parseInt(e.target.value))}
          />
          <button
            className="btn-secondary"
            onClick={() => onChange('seed', -1)}
          >
            🎲 ランダム
          </button>
        </div>
      </div>
      
      {/* バッチサイズ */}
      <div>
        <label className="label">バッチサイズ</label>
        <input
          type="number"
          className="input-field w-full"
          value={settings.batch_size}
          onChange={(e) => onChange('batch_size', parseInt(e.target.value))}
          min="1"
          max="8"
        />
      </div>
    </div>
  )
}

export default GenerationSettings