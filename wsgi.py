import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 股票代碼
STOCK_TICKERS = {
    "hsi": "^HSI",
    "dji": "^DJI",
    "spx": "^GSPC",
    "ixic": "^IXIC",
    "sse": "000001.SS"
}

# 外匯代碼
FX_TICKERS = {
    "usd": "HKDUSD=X",
    "eur": "HKDEUR=X",
    "gbp": "HKDGBP=X",
    "jpy": "HKDJPY=X",
    "cny": "HKDCNY=X"
}

def get_stock_data():
    """只返回 yfinance 真實數據，失敗則返回空"""
    import yfinance as yf
    data = {}
    for key, ticker in STOCK_TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent = ((current - prev_close) / prev_close) * 100
                data[key] = {
                    "price": round(current, 2),
                    "previous_close": round(prev_close, 2),
                    "percent": round(percent, 2)
                }
        except Exception as e:
            pass
    return data

def get_fx_data():
    """只返回 yfinance 真實數據，失敗則返回空"""
    import yfinance as yf
    data = {}
    for key, ticker in FX_TICKERS.items():
        try:
            forex = yf.Ticker(ticker)
            hist = forex.history(period="2d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent = ((current - prev_close) / prev_close) * 100
                data[key] = {
                    "price": round(current, 4),
                    "previous_close": round(prev_close, 4),
                    "percent": round(percent, 2)
                }
        except Exception as e:
            pass
    return data

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/stocks')
def stocks():
    data = get_stock_data()
    if not data:
        return jsonify({"error": "無法獲取股票數據"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    if not data:
        return jsonify({"error": "無法獲取外匯數據"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api", "data_source": "yfinance"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v3.0", "data_source": "yfinance", "no_fallback": True})

application = app
