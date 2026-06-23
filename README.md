# AI Short Drama Studio

本项目是一套可在 Windows 本地网页运行的 **AI 短剧创作工作流系统**，用于把一个短剧脑洞拆解成市场判断、爆款结构、人设、分集大纲、剧本、台词、分镜、视频提示词、美术一致性、合规审核、数据复盘和视频生产任务。

> 目标不是做一个“聊天框许愿机”，而是做一条可迭代的短剧工业流水线。毕竟把创作全塞进一个 Prompt 里，通常只会得到一盆带标题的创意粥。

## 功能

- 后台管理：项目、创作产物、模型配置、视频任务管理。
- 自动化编剧平台：13 个 Agent 角色串联生成短剧生产资料。
- 多模型交叉评审：支持多个大模型从钩子、人设、爽点、反转、台词、可拍性、合规等维度评分。
- 视频生产任务系统：将分镜和视频 Prompt 转为任务，预留 Kling、Runway、Veo、海螺、Seedance 等视频 API 适配入口。
- Windows 本地网页运行：浏览器打开 `http://localhost:5173`。
- Docker 一键启动：自动检测 Docker，优先容器运行。
- 无 API Key 也能演示：启用本地 Mock 结构样稿，便于先验收流程。

## Agent 团队

| 角色 | 任务 | 产物 |
|---|---|---|
| 总导演 / Showrunner | 统一项目方向、卖点、风格和边界 | 项目圣经、情绪曲线、风险清单 |
| 市场雷达专员 | 分析平台趋势、受众痛点和传播机会 | 趋势雷达、封面标题方向、平台打法 |
| 爆款拆解专员 | 拆解同类爆款结构 | 钩子模板、爽点模板、付费点 |
| 脑洞策划专员 | 设计强设定、抽象梗、极端处境 | 高概念脑洞、反转池 |
| 人设专员 | 设计主角、反派、关系网、秘密 | 人物卡、关系冲突图、视觉锚点 |
| 分集大纲专员 | 规划每集钩子、爽点、反转、尾钩 | 分集大纲、情绪曲线 |
| 编剧 | 写可拍摄分场剧本 | 剧本、动作、对白 |
| 台词嘴替专员 | 强化台词网感和传播性 | 金句、预告切片句、嘴替版对白 |
| 分镜导演 | 拆镜头、景别、构图、运镜 | 镜头表、竖屏构图方案 |
| 视频提示词专员 | 生成视频模型 Prompt | 中英双语 Prompt、负面 Prompt |
| 美术资产一致性专员 | 保持角色、场景、服装、道具一致 | 角色资产卡、场景资产卡 |
| 合规审核专员 | 检查平台和内容风险 | 风险等级、修改建议 |
| 数据复盘专员 | 根据数据迭代剧情 | 指标看板、A/B 测试建议 |

## 技术栈

- Backend：FastAPI + SQLAlchemy + SQLite
- Frontend：React + Vite + TypeScript
- LLM：OpenAI-Compatible Provider 抽象层
- Deploy：Docker Compose / Windows PowerShell 本地模式

## 快速启动

### 方式一：Windows 一行启动

在项目根目录打开 PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

脚本会自动：

1. 创建 `.env`。
2. 检测 Docker Compose。
3. 有 Docker 时执行 `docker compose up --build`。
4. 没有 Docker 时使用本地 Python + Node 启动。

启动后打开：

- 前端：`http://localhost:5173`
- 后端 API：`http://localhost:8000/docs`

### 方式二：Docker 手动启动

```powershell
copy .env.example .env
docker compose up --build
```

### 方式三：不用 Docker

```powershell
copy .env.example .env
cd backend
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

另开一个 PowerShell：

```powershell
cd frontend
npm install
npm run dev
```

## 配置大模型 API

复制 `.env.example` 为 `.env` 后填写：

```env
OPENAI_API_KEY=sk-...
XAI_API_KEY=xai-...
SILICONFLOW_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
OPENROUTER_API_KEY=sk-or-...
```

系统默认把这些服务视为 OpenAI-Compatible `/chat/completions` 接口。你也可以在后台添加自定义模型：

- `name`：模型显示名
- `base_url`：如 `https://api.example.com/v1`
- `api_key_env`：如 `CUSTOM_API_KEY`
- `model_name`：实际模型名

## 视频 API 接入位置

当前版本已经有视频任务状态机和 Prompt 管理。真实平台 API 差异很大，建议在这里接入：

```text
backend/app/routers/video.py
```

推荐后续扩展：

```text
backend/app/video_providers/kling.py
backend/app/video_providers/runway.py
backend/app/video_providers/veo.py
backend/app/video_providers/hailuo.py
backend/app/video_providers/seedance.py
```

统一接口建议：

```python
class VideoProvider:
    async def submit(prompt: str, negative_prompt: str, refs: list[dict]) -> str: ...
    async def poll(task_id: str) -> dict: ...
```

## GitHub 上传

当前 ChatGPT GitHub 工具可写已有仓库，但没有“新建仓库”权限。本项目附带 GitHub CLI 推送脚本。

安装并登录 GitHub CLI 后，在项目根目录运行：

```powershell
.\scripts\create-github-repo.ps1 -RepoName ai-short-drama-studio -Owner weeduon
```

或者手动：

```powershell
git init
git add .
git commit -m "Initial AI short drama studio"
gh repo create weeduon/ai-short-drama-studio --private --source . --remote origin --push
```

仓库创建后，远程一行安装命令可写成：

```powershell
irm https://raw.githubusercontent.com/weeduon/ai-short-drama-studio/main/install.ps1 | iex
```

## API 示例

创建项目：

```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"title":"无后之徒：AI族谱开局跪了","logline":"全家嘲笑男主绝后无用，家族AI族谱却认证他是唯一继承人。"}'
```

运行工作流：

```bash
curl -X POST http://localhost:8000/api/projects/1/run \
  -H "Content-Type: application/json" \
  -d '{"episode_count":6,"use_cross_review":true}'
```

多模型交叉评审：

```bash
curl -X POST http://localhost:8000/api/review/cross \
  -H "Content-Type: application/json" \
  -d '{"artifact_id":1}'
```

## 开发路线图

- [ ] 用户登录和权限分组
- [ ] 项目版本管理和回滚
- [ ] 视频 Provider 插件化
- [ ] 剧本导出 Word/PDF
- [ ] 分镜表导出 Excel
- [ ] 接入 Dify / n8n 工作流 Webhook
- [ ] 接入素材库和角色 LoRA / 参考图管理
- [ ] 数据复盘接入抖音/快手/小红书手动 CSV 或 API
- [ ] 一键打包成桌面应用 / PWA

## 注意

- 不要把真实 API Key 提交到 GitHub。
- 不要上传侵犯他人版权或肖像权的素材。
- 不要生成违法、未成年人性化、真实名人伪造、危险指导等内容。
- AI 生成内容必须人工审核。让模型自己审自己，和让猫看鱼摊差不多，至少要多模型交叉。
