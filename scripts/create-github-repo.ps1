param(
  [string]$RepoName = "ai-short-drama-studio",
  [string]$Owner = "weeduon"
)

$ErrorActionPreference = "Stop"
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
  throw "未检测到 GitHub CLI。请安装 gh: https://cli.github.com/"
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "未检测到 git。请先安装 Git。"
}

gh auth status | Out-Null
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Test-Path ".git")) { git init }
git add .
git commit -m "Initial AI short drama studio" 2>$null

gh repo create "$Owner/$RepoName" --private --source . --remote origin --push
Write-Host "已推送到 https://github.com/$Owner/$RepoName" -ForegroundColor Green
