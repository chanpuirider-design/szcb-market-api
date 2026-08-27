import sys
import os
import time
import json
import urllib.request
import urllib.error
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 直接使用 Yahoo Finance API
def fetch_yahoo_data(symbol, period="5d"):
    """直接使用 Yahoo Finance API 獲取數據"""
    try:
        # Yahoo Finance API endpoint
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={int(time.time())-86400*2}&period2={int(time.time())}&interval=1d"
        
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            
            if 'chart' in data and data['chart']['result']:
                result = data['chart']['result'][0]
                timestamps = result['timestamp']
                closes = result['indicators']['quote'][0]['close']
                
                # 過濾掉 None 值
                closes = [c for c in closes if c is not None]
                
                if len(closes) >= 2:
                    current = closes[-1]
                    prev_close = closes[-2]
                    percent = ((current - prev_close) / prev_close) * 100
                    return {
                        "price": round(current, 3),
                        "previous_close": round(prev_close, 3),
                        "percent": round(percent, 2),
                        "price_display": f"{current:.3f}",
                        "previous_close_display": f"{prev_close:.3f}"
                    }
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}", file=sys.stderr)
    
    return None

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
    "usd": "USDHKD=X",
    "eur": "EURHKD=X",
    "gbp": "GBPUSD=X",
    "jpy": "JPYHKD=X",
    "cny": "CNYHKD=X"
}

def get_stock_data():
    """獲取股票數據"""
    data = {}
    for key, symbol in STOCK_TICKERS.items():
        result = fetch_yahoo_data(symbol)
        if result:
            data[key] = result
            print(f"[OK] {key}: {result['price']}", file=sys.stderr)
        else:
            print(f"[WARN] {key}: 無法獲取數據", file=sys.stderr)
    return data

def get_fx_data():
    """獲取外匯數據"""
    data = {}
    for key, symbol in FX_TICKERS.items():
        result = fetch_yahoo_data(symbol)
        if result:
            data[key] = result
            print(f"[OK] {key}: {result['price']}", file=sys.stderr)
        else:
            print(f"[WARN] {key}: 無法獲取數據", file=sys.stderr)
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
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/debug')
def debug():
    results = {
        "python_version": sys.version,
        "test_results": {}
    }
    
    # 測試 Yahoo API
    for symbol in ["^HSI", "USDHKD=X", "^DJI"]:
        try:
            result = fetch_yahoo_data(symbol)
            results["test_results"][symbol] = result
        except Exception as e:
            results["test_results"][symbol] = {"error": str(e)}
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v5.0", "data_source": "Yahoo Finance API"})

application = app
