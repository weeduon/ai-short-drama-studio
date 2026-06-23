const API_BASE = import.meta.env.VITE_API_BASE || ''

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export type Project = {
  id: number
  title: string
  logline: string
  genre: string
  audience: string
  platform: string
  tone: string
  status: string
  created_at: string
  updated_at: string
}

export type Artifact = {
  id: number
  project_id: number
  stage: string
  role: string
  title: string
  content: Record<string, unknown>
  score?: Record<string, unknown> | null
  created_at: string
}

export type Role = {
  key: string
  name: string
  mission: string
  output: string
  quality_bar: string
}

export type VideoTask = {
  id: number
  project_id: number
  episode: number
  scene_no: number
  provider: string
  status: string
  prompt: string
  negative_prompt: string
  result_url?: string | null
  error?: string | null
}

export const api = {
  health: () => request<{ status: string }>('/health'),
  roles: () => request<Role[]>('/api/roles'),
  projects: () => request<Project[]>('/api/projects'),
  createProject: (payload: Partial<Project>) => request<Project>('/api/projects', { method: 'POST', body: JSON.stringify(payload) }),
  artifacts: (projectId: number) => request<Artifact[]>(`/api/projects/${projectId}/artifacts`),
  runWorkflow: (projectId: number, episodeCount: number) => request<Artifact[]>(`/api/projects/${projectId}/run`, { method: 'POST', body: JSON.stringify({ episode_count: episodeCount, use_cross_review: true }) }),
  crossReview: (artifactId: number) => request<Record<string, unknown>>('/api/review/cross', { method: 'POST', body: JSON.stringify({ artifact_id: artifactId }) }),
  videoTasks: (projectId?: number) => request<VideoTask[]>(`/api/video-tasks${projectId ? `?project_id=${projectId}` : ''}`),
  createVideoTask: (payload: Record<string, unknown>) => request<VideoTask>('/api/video-tasks', { method: 'POST', body: JSON.stringify(payload) }),
  runVideoTask: (id: number) => request<VideoTask>(`/api/video-tasks/${id}/run`, { method: 'POST' }),
}
