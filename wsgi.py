"""
SHCB Market Data API - FastAPI + Yahoo Finance (PythonAnywhere WSGI 兼容版本)
"""

import sys
import os
from flask import Flask, jsonify

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 導入 FastAPI 應用和函數
from main import get_stocks, get_fx_rates, health_check

# 註冊路由
@app.route('/api/stocks')
def stocks():
    """獲取股票數據"""
    try:
        data = get_stocks()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fx-rates')
def fx_rates():
    """獲取匯率數據"""
    try:
        data = get_fx_rates()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yahoo/ticker/<ticker>')
def yahoo_ticker(ticker):
    """獲取單一股票數據"""
    try:
        from main import get_yahoo_data
        data = get_yahoo_data(ticker)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """健康檢查"""
    try:
        data = health_check()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
@app.route('/docs')
@app.route('/redoc')
def index():
    """API 首頁"""
    return jsonify({
        "message": "SHCB Market Data API",
        "version": "1.0.0",
        "endpoints": [
            "/api/stocks",
            "/api/fx-rates",
            "/api/yahoo/ticker/{ticker}",
            "/health"
        ]
    })

# WSGI 入口
application = app
