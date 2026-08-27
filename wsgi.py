import sys
import os
from flask import Flask, jsonify

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 簡單路由
@app.route('/api/stocks')
def stocks():
    try:
        return jsonify({
            "hsi": {"price": 22500.50, "change": "+1.2%"},
            "dji": {"price": 38000.00, "change": "+0.8%"},
            "spx": {"price": 5200.00, "change": "+0.5%"}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fx-rates')
def fx_rates():
    try:
        return jsonify({
            "usd": {"price": 7.82, "change": "+0.01%"},
            "eur": {"price": 8.50, "change": "-0.02%"},
            "gbp": {"price": 9.90, "change": "+0.03%"}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "shcb-market-api"
    })

@app.route('/')
@app.route('/docs')
@app.route('/redoc')
def index():
    return jsonify({
        "message": "SHCB Market Data API",
        "version": "1.0.0",
        "endpoints": [
            "/api/stocks",
            "/api/fx-rates",
            "/health"
        ]
    })

# WSGI 入口
application = app
