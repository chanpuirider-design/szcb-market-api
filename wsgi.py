import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 已驗證的正確 ticker 格式（從 PythonAnywhere 測試確認）
STOCK_TICKERS = {
    "hsi": "^HSI",
    "dji": "^DJI",
    "spx": "^GSPC",
    "ixic": "^IXIC",
    "sse": "000001.SS"
}

FX_TICKERS = {
    "usd": "USDHKD=X",
    "eur": "EURHKD=X",
    "gbp": "GBPUSD=X",
    "jpy": "JPYHKD=X",
    "cny": "CNHHKD=X"
}

def get_stock_data():
    """獲取股票數據"""
    import yfinance as yf
    data = {}
    for key, ticker in STOCK_TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent = ((current - prev_close) / prev_close) * 100
                data[key] = {
                    "price": round(current, 2),
                    "previous_close": round(prev_close, 2),
                    "percent": round(percent, 2)
                }
                print(f"[OK] {key}: {current}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] {key}: {e}", file=sys.stderr)
    return data

def get_fx_data():
    """獲取外匯數據"""
    import yfinance as yf
    data = {}
    for key, ticker in FX_TICKERS.items():
        try:
            forex = yf.Ticker(ticker)
            hist = forex.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent = ((current - prev_close) / prev_close) * 100
                data[key] = {
                    "price": round(current, 4),
                    "previous_close": round(prev_close, 4),
                    "percent": round(percent, 2)
                }
                print(f"[OK] {key}: {current}", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] {key}: {e}", file=sys.stderr)
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
    import yfinance as yf
    results = {}
    
    # 測試所有 ticker
    for name, ticker in {**STOCK_TICKERS, **FX_TICKERS}.items():
        try:
            t = yf.Ticker(ticker)
            h = t.history(period="5d")
            results[ticker] = {
                "name": name,
                "rows": len(h),
                "last_price": float(h['Close'].iloc[-1]) if not h.empty else None
            }
        except Exception as e:
            results[ticker] = {"name": name, "error": str(e)}
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v4.1", "data_source": "yfinance"})

application = app
