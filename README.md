# AI Short Drama Studio

一套可在 Windows 本地网页运行的 AI 短剧创作工作流系统。它把一个短剧创意拆成市场判断、爆款结构、人设、分集大纲、剧本、台词、分镜、视频提示词、美术一致性、合规审核、数据复盘和视频生产任务。终于，人类连脑洞都要流水线化，效率怪兽又赢了一局。

## 功能

- 后台管理：项目、创作产物、模型配置、视频任务。
- 自动化编剧平台：13 个 Agent 角色串联生成短剧生产资料。
- 多模型交叉评审：多个模型从钩子、人设、爽点、反转、台词、可拍性、合规等维度评分。
- 视频生产任务系统：将分镜和视频 Prompt 转为任务，预留可灵、Runway、Veo、海螺、Seedance 等平台接入位置。
- 本地运行：Windows 浏览器访问 `http://localhost:5173`。
- Docker 优先：安装脚本会自动检测 Docker Compose。
- 无 API Key 演示：没有模型密钥时使用本地 Mock 样稿。

## Agent 团队

| 角色 | 任务 | 产物 |
|---|---|---|
| 总导演 / Showrunner | 统一定位、卖点、风格和边界 | 项目圣经、情绪曲线 |
| 市场雷达专员 | 判断平台趋势、受众痛点 | 趋势雷达、标题方向 |
| 爆款拆解专员 | 拆解同类爆款结构 | 钩子模板、爽点模板 |
| 脑洞策划专员 | 设计强设定和反转 | 高概念脑洞、反转池 |
| 人设专员 | 设计主角、反派、关系网 | 人物卡、视觉锚点 |
| 分集大纲专员 | 规划每集钩子、爽点、尾钩 | 分集大纲 |
| 编剧 | 写可拍摄分场剧本 | 剧本、动作、对白 |
| 台词嘴替专员 | 强化台词网感和传播性 | 金句、切片句 |
| 分镜导演 | 拆镜头、景别、构图、运镜 | 镜头表 |
| 视频提示词专员 | 生成视频模型 Prompt | 中英双语 Prompt |
| 美术资产一致性专员 | 保持角色、场景、服装一致 | 资产卡 |
| 合规审核专员 | 检查内容和平台风险 | 风险等级、修改建议 |
| 数据复盘专员 | 根据数据迭代剧情 | A/B 测试和复盘方案 |

## 技术栈

- Backend：FastAPI + SQLAlchemy + SQLite
- Frontend：React + Vite + TypeScript
- LLM：OpenAI-Compatible Provider 抽象层
- Deploy：Docker Compose / Windows PowerShell

## 快速启动

### Windows 一键启动

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

启动后访问：

- 前端：`http://localhost:5173`
- 后端 API：`http://localhost:8000/docs`

### Docker 手动启动

```powershell
copy .env.example .env
docker compose up --build
```

### 不用 Docker

第一个 PowerShell：

```powershell
copy .env.example .env
cd backend
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

第二个 PowerShell：

```powershell
cd frontend
npm install
$env:VITE_API_BASE='http://127.0.0.1:8000'
npx vite --host 0.0.0.0
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

系统默认使用 OpenAI-Compatible `/chat/completions` 协议。也可以在后台添加自定义模型：

```json
{
  "name": "My API",
  "provider_type": "openai_compatible",
  "base_url": "https://api.example.com/v1",
  "api_key_env": "CUSTOM_API_KEY",
  "model_name": "my-model",
  "enabled": true,
  "purpose": "writing"
}
```

## 视频 API 接入位置

当前版本已经有视频任务状态机和 Prompt 管理。真实视频平台 API 差异较大，建议在这里扩展：

```text
backend/app/routers/video.py
backend/app/video_providers/kling.py
backend/app/video_providers/runway.py
backend/app/video_providers/veo.py
backend/app/video_providers/hailuo.py
backend/app/video_providers/seedance.py
```

## 远程一行安装

仓库公开后，可以在 Windows PowerShell 使用：

```powershell
irm https://raw.githubusercontent.com/weeduon/ai-short-drama-studio/main/install.ps1 | iex
```

## API 示例

```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"title":"AI短剧项目","logline":"一个主角在关键场合获得新身份信息，并推动连续反转。"}'
```

```bash
curl -X POST http://localhost:8000/api/projects/1/run \
  -H "Content-Type: application/json" \
  -d '{"episode_count":6,"use_cross_review":true}'
```

```bash
curl -X POST http://localhost:8000/api/review/cross \
  -H "Content-Type: application/json" \
  -d '{"artifact_id":1}'
```

## 路线图

- 用户登录和权限分组
- 项目版本管理和回滚
- 视频 Provider 插件化
- 剧本导出 Word/PDF
- 分镜表导出 Excel
- 接入 Dify / n8n Webhook
- 接入素材库和角色一致性参考图
- 数据复盘接入短视频平台手动 CSV 或 API
- 打包成桌面应用 / PWA

## 注意

- 不要把真实 API Key 提交到 GitHub。
- AI 生成内容必须人工审核。
- 真实上线前请补充登录、权限、审计日志和数据保留策略。
