import sys
import os
from flask import Flask, Response, jsonify, request as flask_request

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 導入 FastAPI 應用和函數
from main import app as fastapi_app
from main import get_stock_data, get_fx_rates, health_check

# 註冊路由
@app.route('/api/stocks')
@app.route('/api/fx-rates')
@app.route('/health')
@app.route('/')
@app.route('/docs')
@app.route('/redoc')
def handle_api():
    path = flask_request.path
    
    if path == '/api/stocks':
        data = get_stock_data()
        return jsonify(data)
    elif path == '/api/fx-rates':
        data = get_fx_rates()
        return jsonify(data)
    elif path == '/health':
        data = health_check()
        return jsonify(data)
    elif path in ['/docs', '/redoc']:
        return Response(
            '<html><body><h1>API Documentation</h1><p>Use the <code>GET</code> endpoints:</p>'
            '<ul><li><a href="/api/stocks">/api/stocks</a></li>'
            '<li><a href="/api/fx-rates">/api/fx-rates</a></li></ul></body></html>',
            mimetype='text/html'
        )
    else:
        return jsonify({
            "message": "SHCB Market Data API",
            "version": "1.0.0",
            "endpoints": ["/api/stocks", "/api/fx-rates", "/health"]
        })

# WSGI 入口
application = app
