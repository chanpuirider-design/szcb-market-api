"""
SHCB Market Data API - 簡單 Flask 包裝器
為 PythonAnywhere WSGI 兼容而設計
"""

import sys
import os
from flask import Flask, jsonify

# 應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 導入 FastAPI 函數
from main import get_stock_data, get_fx_rates, health_check

# 路由定義
@app.route('/api/stocks')
def api_stocks():
    """獲取股票數據"""
    return jsonify(get_stock_data())

@app.route('/api/fx-rates')
def api_fx_rates():
    """獲取匯率數據"""
    return jsonify(get_fx_rates())

@app.route('/health')
def api_health():
    """健康檢查"""
    return jsonify(health_check())

@app.route('/')
@app.route('/docs')
@app.route('/redoc')
def api_index():
    """API 首頁"""
    return jsonify({
        "message": "SHCB Market Data API",
        "version": "1.0.0",
        "endpoints": [
            "/api/stocks",
            "/api/fx-rates",
            "/health"
        ]
    })

# WSGI 入口點
application = app
