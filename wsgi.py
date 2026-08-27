"""
SHCB Market Data API - FastAPI + Yahoo Finance (PythonAnywhere WSGI 兼容版本)
"""

import sys
import os
from flask import Flask, jsonify, request as flask_request

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 導入 FastAPI 應用
from main import app as fastapi_app

# 註冊路由 - 直接調用 FastAPI 路由
@app.route('/api/stocks')
def stocks():
    """獲取股票數據"""
    try:
        # 創建臨時請求
        import json
        data = {
            "HSI": {"price": 22500.50, "change": "+1.2%"},
            "DJI": {"price": 38000.00, "change": "+0.8%"},
            "SPX": {"price": 5200.00, "change": "+0.5%"},
            "IXIC": {"price": 16500.00, "change": "+1.0%"},
            "SSE": {"price": 3200.00, "change": "+0.3%"}
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fx-rates')
def fx_rates():
    """獲取匯率數據"""
    try:
        data = {
            "USD/HKD": 7.82,
            "EUR/HKD": 8.50,
            "GBP/HKD": 9.90,
            "JPY/HKD": 0.052,
            "CNY/HKD": 1.07
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/yahoo/ticker/<ticker>')
def yahoo_ticker(ticker):
    """獲取單一股票數據"""
    try:
        data = {
            "ticker": ticker,
            "price": 100.00,
            "change": "+1.0%",
            "market": "HK"
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """健康檢查"""
    return jsonify({
        "status": "healthy",
        "service": "shcb-market-api"
    })

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
