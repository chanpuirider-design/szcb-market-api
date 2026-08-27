import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 簡單的硬編碼數據 - 立即返回
STOCK_DATA = {
    "hsi": {"price": 22500.50, "previous_close": 22230.00, "percent": 1.22},
    "dji": {"price": 38000.00, "previous_close": 37700.00, "percent": 0.80},
    "spx": {"price": 5200.00, "previous_close": 5175.00, "percent": 0.48},
    "ixic": {"price": 16500.00, "previous_close": 16350.00, "percent": 0.92},
    "sse": {"price": 3200.00, "previous_close": 3190.00, "percent": 0.31}
}

FX_DATA = {
    "usd": {"price": 7.82, "previous_close": 7.81, "percent": 0.13},
    "eur": {"price": 8.50, "previous_close": 8.48, "percent": 0.24},
    "gbp": {"price": 9.90, "previous_close": 9.88, "percent": 0.20},
    "jpy": {"price": 0.0521, "previous_close": 0.0520, "percent": 0.19},
    "cny": {"price": 1.07, "previous_close": 1.07, "percent": 0.00}
}

@app.route('/api/stocks')
def stocks():
    return jsonify(STOCK_DATA)

@app.route('/api/fx-rates')
def fx_rates():
    return jsonify(FX_DATA)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

application = app
