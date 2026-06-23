import { useEffect, useState } from 'react'
import { api, Artifact, Project, Role, VideoTask } from './api'
import './styles.css'

export default function App() {
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

  useEffect(() => {
    refresh().catch((err) => setMessage(err.message))
  }, [])

  useEffect(() => {
    loadProject().catch((err) => setMessage(err.message))
  }, [selectedId])

  async function createProject() {
    setBusy(true)
    try {
      const project = await api.createProject(form)
      setSelectedId(project.id)
      await refresh()
      setMessage('项目已创建')
    } catch (err) {
      setMessage((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  async function runWorkflow() {
    if (!selected) return
    setBusy(true)
    try {
      setArtifacts(await api.runWorkflow(selected.id, 6))
      setMessage('工作流已完成')
    } catch (err) {
      setMessage((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  async function reviewArtifact(artifact: Artifact) {
    setBusy(true)
    try {
      await api.crossReview(artifact.id)
      await loadProject()
      setMessage('评审完成')
    } catch (err) {
      setMessage((err as Error).message)
    } finally {
      setBusy(false)
    }
  }

  async function createTask(artifact: Artifact) {
    if (!selected) return
    const content = JSON.stringify(artifact.content)
    await api.createVideoTask({ project_id: selected.id, episode: 1, scene_no: 1, provider: 'manual', prompt: content.slice(0, 1000), negative_prompt: 'blurry, watermark' })
    await loadProject()
    setMessage('视频任务已创建')
  }

  return (
    <div className="app">
      <aside>
        <h1>AI Short Drama Studio</h1>
        <p>本地短剧工作流后台。终于把灵感这种不稳定燃料装进了管道里。</p>
        <h3>项目</h3>
        {projects.map((project) => <button key={project.id} onClick={() => setSelectedId(project.id)}>{project.title}</button>)}
      </aside>
      <main>
        <header>
          <div>
            <h2>{selected?.title || '创建项目'}</h2>
            <p>{selected?.logline || '从创意到分镜、提示词、评审和视频任务。'}</p>
          </div>
          <span>{busy ? '处理中' : '本地运行'}</span>
        </header>
        {message && <div className="message">{message}</div>}
        <section className="grid">
          <div className="card">
            <h3>新建项目</h3>
            {Object.entries(form).map(([key, value]) => (
              <label key={key}>{key}<textarea value={value} onChange={(event) => setForm({ ...form, [key]: event.target.value })} /></label>
            ))}
            <button onClick={createProject}>创建项目</button>
          </div>
          <div className="card">
            <h3>工作流</h3>
            <button disabled={!selected || busy} onClick={runWorkflow}>运行 Agent 团队</button>
            <p>总导演、市场雷达、爆款拆解、脑洞策划、人设、分集大纲、编剧、台词、分镜、提示词、美术一致性、合规、数据复盘。</p>
          </div>
        </section>
        <section className="card full">
          <h3>创作产物</h3>
          {artifacts.map((artifact) => (
            <article className="artifact" key={artifact.id}>
              <b>{artifact.role}</b>
              <small>{artifact.stage}</small>
              <div className="actions"><button onClick={() => reviewArtifact(artifact)}>交叉评审</button><button onClick={() => createTask(artifact)}>生成视频任务</button></div>
              <pre>{JSON.stringify(artifact.content, null, 2)}</pre>
            </article>
          ))}
        </section>
        <section className="card full">
          <h3>视频任务</h3>
          {tasks.map((task) => <article className="task" key={task.id}><b>{task.provider}</b><small>{task.status}</small><p>{task.prompt}</p></article>)}
        </section>
        <section className="card full">
          <h3>Agent 团队</h3>
          <div className="roles">{roles.map((role) => <div key={role.key}><b>{role.name}</b><p>{role.mission}</p></div>)}</div>
        </section>
      </main>
    </div>
  )
}
