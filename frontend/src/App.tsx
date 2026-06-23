import { useEffect, useState } from 'react'
import { Bot, Clapperboard, Film, LayoutDashboard, WandSparkles } from 'lucide-react'
import { api, Artifact, Project, Role, VideoTask } from './api'
import ModelSettings from './ModelSettings'
import './styles.css'

type Tab = 'studio' | 'models' | 'guide'

export default function App() {
  const [tab, setTab] = useState<Tab>('studio')
  const [roles, setRoles] = useState<Role[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [artifacts, setArtifacts] = useState<Artifact[]>([])
  const [tasks, setTasks] = useState<VideoTask[]>([])
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)
  const [form, setForm] = useState({
    title: 'AI短剧项目',
    logline: '一个主角在关键场合获得新身份信息，并由此推动连续反转。',
    genre: '竖屏短剧',
    audience: '短剧用户',
    platform: '9:16 竖屏',
    tone: '强设定、强反转、快节奏',
  })

  const selected = projects.find((item) => item.id === selectedId)

  async function refresh() {
    const [roleData, projectData] = await Promise.all([api.roles(), api.projects()])
    setRoles(roleData)
    setProjects(projectData)
    if (!selectedId && projectData[0]) setSelectedId(projectData[0].id)
  }

  async function loadProject(id = selectedId) {
    if (!id) return
    setArtifacts(await api.artifacts(id))
    setTasks(await api.videoTasks(id))
  }

  useEffect(() => { refresh().catch((err) => setMessage(err.message)) }, [])
  useEffect(() => { loadProject().catch((err) => setMessage(err.message)) }, [selectedId])

  async function createProject() {
    setBusy(true)
    try {
      const project = await api.createProject(form)
      setSelectedId(project.id)
      await refresh()
      setMessage('项目已创建，下一步点“运行 Agent 团队”。')
    } catch (err) { setMessage((err as Error).message) } finally { setBusy(false) }
  }

  async function runWorkflow() {
    if (!selected) return
    setBusy(true)
    try {
      setArtifacts(await api.runWorkflow(selected.id, 6))
      setMessage('工作流已完成。现在可以评审产物或生成视频任务。')
    } catch (err) { setMessage((err as Error).message) } finally { setBusy(false) }
  }

  async function reviewArtifact(artifact: Artifact) {
    setBusy(true)
    try {
      await api.crossReview(artifact.id)
      await loadProject()
      setMessage('多模型交叉评审完成。')
    } catch (err) { setMessage((err as Error).message) } finally { setBusy(false) }
  }

  async function createTask(artifact: Artifact) {
    if (!selected) return
    const content = JSON.stringify(artifact.content)
    await api.createVideoTask({ project_id: selected.id, episode: 1, scene_no: 1, provider: 'manual', prompt: content.slice(0, 1000), negative_prompt: 'blurry, watermark' })
    await loadProject()
    setMessage('视频任务已创建。')
  }

  return (
    <div className="app shell">
      <aside>
        <div className="brand"><div className="logo"><Clapperboard size={24} /></div><div><h1>AI Short Drama Studio</h1><p>新手友好的短剧工业工作台</p></div></div>
        <nav className="nav">
          <button className={tab === 'studio' ? 'active' : ''} onClick={() => setTab('studio')}><LayoutDashboard size={18} /> 创作台</button>
          <button className={tab === 'models' ? 'active' : ''} onClick={() => setTab('models')}><Bot size={18} /> 模型配置</button>
          <button className={tab === 'guide' ? 'active' : ''} onClick={() => setTab('guide')}><WandSparkles size={18} /> 新手向导</button>
        </nav>
        <h3>项目列表</h3>
        {projects.length === 0 && <p className="muted">还没有项目，先在创作台创建一个。文明又一次从表单开始。</p>}
        {projects.map((project) => <button className="projectBtn" key={project.id} onClick={() => setSelectedId(project.id)}>{project.title}</button>)}
      </aside>

      <main>
        {tab === 'studio' && (
          <>
            <header className="topbar">
              <div>
                <span className="eyebrow"><Film size={16} /> AI 短剧生产线</span>
                <h2>{selected?.title || '创建你的第一个短剧项目'}</h2>
                <p>{selected?.logline || '从创意到剧本、分镜、视频提示词和任务队列。'}</p>
              </div>
              <span className="pill">{busy ? '处理中' : '本地运行'}</span>
            </header>
            {message && <div className="message">{message}</div>}

            <section className="grid">
              <div className="card glass">
                <h3>1. 新建项目</h3>
                {Object.entries(form).map(([key, value]) => (
                  <label key={key}>{key}<textarea value={value} onChange={(event) => setForm({ ...form, [key]: event.target.value })} /></label>
                ))}
                <button onClick={createProject}>创建项目</button>
              </div>
              <div className="card glass">
                <h3>2. 运行 Agent 团队</h3>
                <p>系统会按“市场判断 → 爆款拆解 → 脑洞 → 人设 → 分集 → 剧本 → 台词 → 分镜 → 视频 Prompt → 合规 → 复盘”的顺序生成资料。</p>
                <button disabled={!selected || busy} onClick={runWorkflow}>运行 13 个 Agent</button>
                <div className="miniStats"><span>{roles.length} 个角色</span><span>{artifacts.length} 个产物</span><span>{tasks.length} 个视频任务</span></div>
              </div>
            </section>

            <section className="card full">
              <h3>3. 创作产物</h3>
              {artifacts.map((artifact) => (
                <article className="artifact" key={artifact.id}>
                  <div className="artifactHead"><div><b>{artifact.role}</b><small>{artifact.stage}</small></div><div className="actions"><button onClick={() => reviewArtifact(artifact)}>交叉评审</button><button onClick={() => createTask(artifact)}>生成视频任务</button></div></div>
                  <pre>{JSON.stringify(artifact.content, null, 2)}</pre>
                </article>
              ))}
            </section>

            <section className="card full">
              <h3>4. 视频任务</h3>
              {tasks.map((task) => <article className="task" key={task.id}><b>{task.provider}</b><small>{task.status}</small><p>{task.prompt}</p></article>)}
            </section>
          </>
        )}

        {tab === 'models' && <ModelSettings />}

        {tab === 'guide' && (
          <section className="card full guide">
            <span className="eyebrow"><WandSparkles size={16} /> 小白流程</span>
            <h2>从 0 到第一版 AI 短剧</h2>
            <ol>
              <li><b>模型配置：</b>进入“模型配置”，填 API Key，点测试连接。</li>
              <li><b>创建项目：</b>写短剧名和一句话故事，其他字段不会写就保留默认。</li>
              <li><b>运行 Agent：</b>让系统自动生成市场、脑洞、人设、大纲、剧本和提示词。</li>
              <li><b>交叉评审：</b>对关键产物点“交叉评审”，找出问题。</li>
              <li><b>视频任务：</b>把视频提示词转成任务，再接可灵、Runway、Veo 等平台。</li>
            </ol>
            <div className="roles">{roles.map((role) => <div key={role.key}><b>{role.name}</b><p>{role.mission}</p></div>)}</div>
          </section>
        )}
      </main>
    </div>
  )
}
