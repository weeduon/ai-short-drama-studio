import { useEffect, useState } from 'react'
import { CheckCircle2, PlugZap, Save, TestTube2 } from 'lucide-react'
import { api, ModelProvider } from './api'

type Draft = Partial<ModelProvider> & { apiKey?: string }

const starterTips = [
  '先填 API Key，再点保存密钥。',
  'base_url 一般以 /v1 结尾，例如 https://api.openai.com/v1。',
  'model_name 要填服务商真实支持的模型名。',
  '测试通过后，再回到创作台运行 Agent。',
]

export default function ModelSettings() {
  const [models, setModels] = useState<ModelProvider[]>([])
  const [draft, setDraft] = useState<Draft>({
    name: '自定义模型',
    provider_type: 'openai_compatible',
    base_url: 'https://api.example.com/v1',
    api_key_env: 'CUSTOM_API_KEY',
    model_name: 'your-model-name',
    enabled: true,
    is_default: false,
    purpose: 'writing',
  })
  const [message, setMessage] = useState('')
  const [busyId, setBusyId] = useState<number | null>(null)

  async function load() {
    setModels(await api.models())
  }

  useEffect(() => {
    load().catch((err) => setMessage(err.message))
  }, [])

  async function saveModel() {
    const saved = await api.saveModel(draft)
    setMessage(`已保存模型配置：${saved.name}`)
    setDraft({ ...draft, id: saved.id })
    await load()
  }

  async function saveKey(model: ModelProvider, apiKey: string) {
    if (!apiKey.trim()) {
      setMessage('请先输入 API Key。人类经常忘这一步，模型也不能靠空气付费。')
      return
    }
    setBusyId(model.id)
    try {
      await api.saveModelSecret(model.id, apiKey)
      setMessage(`已保存 ${model.name} 的 API Key。密钥只保存在本地 data/model_keys.json。`)
      await load()
    } catch (err) {
      setMessage((err as Error).message)
    } finally {
      setBusyId(null)
    }
  }

  async function test(model: ModelProvider) {
    setBusyId(model.id)
    try {
      const result = await api.testModel(model.id)
      setMessage(`${model.name} 测试成功：${result.reply}`)
    } catch (err) {
      setMessage((err as Error).message)
    } finally {
      setBusyId(null)
    }
  }

  return (
    <section className="settingsPage">
      <div className="heroPanel">
        <div>
          <span className="eyebrow"><PlugZap size={16} /> 模型接入向导</span>
          <h2>在前端直接配置多家大模型 API</h2>
          <p>适合新手：不用改代码，不用翻后端文件。填地址、模型名、密钥，保存后就能让 Agent 团队调用。</p>
        </div>
        <div className="tipBox">
          {starterTips.map((tip) => <p key={tip}>✓ {tip}</p>)}
        </div>
      </div>

      {message && <div className="message">{message}</div>}

      <div className="grid settingsGrid">
        <div className="card">
          <h3>新增 / 修改模型</h3>
          <label>显示名称<input value={draft.name || ''} onChange={(e) => setDraft({ ...draft, name: e.target.value })} /></label>
          <label>接口地址 base_url<input value={draft.base_url || ''} onChange={(e) => setDraft({ ...draft, base_url: e.target.value })} /></label>
          <label>模型名 model_name<input value={draft.model_name || ''} onChange={(e) => setDraft({ ...draft, model_name: e.target.value })} /></label>
          <label>密钥变量名 api_key_env<input value={draft.api_key_env || ''} onChange={(e) => setDraft({ ...draft, api_key_env: e.target.value.toUpperCase().replace(/[^A-Z0-9_]/g, '_') })} /></label>
          <label>用途
            <select value={draft.purpose || 'writing'} onChange={(e) => setDraft({ ...draft, purpose: e.target.value })}>
              <option value="writing">创作写作</option>
              <option value="review">交叉评审</option>
              <option value="video_prompt">视频提示词</option>
            </select>
          </label>
          <label className="toggle"><input type="checkbox" checked={draft.enabled ?? true} onChange={(e) => setDraft({ ...draft, enabled: e.target.checked })} />启用这个模型</label>
          <button onClick={saveModel}><Save size={16} /> 保存模型配置</button>
        </div>

        <div className="card modelHelp">
          <h3>常见服务商参考</h3>
          <div><b>OpenAI</b><small>https://api.openai.com/v1</small><span>gpt-4.1-mini</span></div>
          <div><b>Grok / xAI</b><small>https://api.x.ai/v1</small><span>grok-3-mini</span></div>
          <div><b>硅基流动</b><small>https://api.siliconflow.cn/v1</small><span>Qwen/Qwen2.5-72B-Instruct</span></div>
          <div><b>DeepSeek</b><small>https://api.deepseek.com/v1</small><span>deepseek-chat</span></div>
          <p>不同平台模型名会变，别靠玄学猜，去服务商后台复制。是的，复制粘贴依旧是现代技术栈的地基。</p>
        </div>
      </div>

      <div className="modelList">
        {models.map((model) => {
          let keyValue = ''
          return (
            <article className="modelCard" key={model.id}>
              <div className="modelTitle">
                <div>
                  <b>{model.name}</b>
                  <small>{model.base_url}</small>
                </div>
                <span className={model.has_api_key ? 'status ok' : 'status'}>{model.has_api_key ? '已配置密钥' : '未配置密钥'}</span>
              </div>
              <div className="modelMeta">
                <span>{model.model_name}</span><span>{model.api_key_env}</span><span>{model.purpose}</span>
              </div>
              <label>API Key<input type="password" placeholder="粘贴密钥，保存后不会在页面显示" onChange={(e) => { keyValue = e.target.value }} /></label>
              <div className="actions">
                <button disabled={busyId === model.id} onClick={() => saveKey(model, keyValue)}><CheckCircle2 size={16} /> 保存密钥</button>
                <button disabled={busyId === model.id || !model.has_api_key} onClick={() => test(model)}><TestTube2 size={16} /> 测试连接</button>
              </div>
            </article>
          )
        })}
      </div>
    </section>
  )
}
