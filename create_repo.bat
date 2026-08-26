@echo off
REM GitHub Personal Access Token - 请替换为你自己的Token
set GITHUB_TOKEN=YOUR_TOKEN_HERE

REM GitHub用户名
set GITHUB_USER=chanpuirider-design

REM 仓库名称
set REPO_NAME=szcb-market-api

REM 创建仓库
echo 正在创建GitHub仓库...
curl -s -X POST ^
  https://api.github.com/user/repos ^
  -H "Authorization: token %GITHUB_TOKEN%" ^
  -H "Accept: application/vnd.github.v3+json" ^
  -d "{\"name\": \"%REPO_NAME%\", \"description\": \"SHCB Market Data API - FastAPI + yfinance\", \"private\": false}"

echo 仓库创建完成！
pause
