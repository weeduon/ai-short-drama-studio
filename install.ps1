param(
  [switch]$NoDocker
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Root) { $Root = (Get-Location).Path }
Set-Location $Root

Write-Host "AI Short Drama Studio installer" -ForegroundColor Cyan
Write-Host "路径: $Root"

if (-not (Test-Path ".env")) {
  Copy-Item ".env.example" ".env"
  Write-Host "已创建 .env，请按需填写 API Key。"
}

function HasCommand($name) {
  return $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

if (-not $NoDocker -and (HasCommand "docker")) {
  try {
    docker compose version | Out-Null
    Write-Host "检测到 Docker Compose，使用容器启动。" -ForegroundColor Green
    docker compose up --build
    exit $LASTEXITCODE
  } catch {
    Write-Host "Docker Compose 不可用，切换到本地 Node/Python 启动。" -ForegroundColor Yellow
  }
}

if (-not (HasCommand "python")) { throw "未检测到 Python。请安装 Python 3.11+，或安装 Docker Desktop。" }
if (-not (HasCommand "node")) { throw "未检测到 Node.js。请安装 Node.js 20+，或安装 Docker Desktop。" }
if (-not (HasCommand "npm")) { throw "未检测到 npm。请安装 Node.js 20+，或安装 Docker Desktop。" }

Write-Host "使用本地模式启动后端和前端。" -ForegroundColor Green

Set-Location "$Root\backend"
if (-not (Test-Path ".venv")) { python -m venv .venv }
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\pip.exe" install -r requirements.txt

Set-Location "$Root\frontend"
npm install

Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root\backend'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$Root\frontend'; npm run dev"

Write-Host "已启动：" -ForegroundColor Cyan
Write-Host "前端: http://localhost:5173"
Write-Host "后端: http://localhost:8000/docs"
