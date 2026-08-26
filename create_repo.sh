#!/bin/bash
# GitHub API Token - 请替换为你自己的Personal Access Token
GITHUB_TOKEN=""

# GitHub用户名
GITHUB_USER="chanpuirider-design"

# 仓库名称
REPO_NAME="szcb-market-api"

# 创建仓库
echo "正在创建GitHub仓库..."
curl -s -X POST \
  https://api.github.com/user/repos \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"SHCB Market Data API - FastAPI + yfinance\",
    \"private\": false
  }"

echo "仓库创建完成！"
