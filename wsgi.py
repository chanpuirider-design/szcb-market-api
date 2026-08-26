"""
PythonAnywhere WSGI configuration for FastAPI
請將此文件複製到 /home/YOUR_USERNAME/szcb-market-api/wsgi.py
"""
import sys
import os

# 添加應用目錄到 Python 路徑
sys.path.insert(0, '/home/YOUR_USERNAME/szcb-market-api')
os.chdir('/home/YOUR_USERNAME/szcb-market-api')

# 導入 FastAPI 應用
from main import app

# PythonAnywhere 需要這個變量
application = app
