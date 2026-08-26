#!/usr/bin/env python3
"""
PythonAnywhere WSGI configuration for FastAPI

安裝步驟:
1. 在 PythonAnywhere 控制台執行: git clone https://github.com/chanpuirider-design/szcb-market-api.git
2. 進入目錄: cd szcb-market-api
3. 創建虛擬環境: python3.11 -m venv venv
4. 激活虛擬環境: source venv/bin/activate
5. 安裝依賴: pip install -r requirements.txt
6. 在 Web 頁面配置 WSGI (見下方)
"""
import sys
import os

# ==================== 配置區 ====================
# 請將 YOUR_USERNAME 替換為你的 PythonAnywhere 用戶名
APP_DIR = '/home/YOUR_USERNAME/szcb-market-api'
# ==================== 配置區 ====================

# 添加應用目錄到 Python 路徑
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 導入 FastAPI 應用
from main import app

# PythonAnywhere 需要這個變量
application = app
