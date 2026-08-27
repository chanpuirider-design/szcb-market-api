import sys
import os
from flask import Flask, jsonify, make_response

# 確保路徑正確
APP_DIR = '/home/chanpuirider/szcb-market-api'
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

print(f"[INIT] APP_DIR: {APP_DIR}", file=sys.stderr)
print(f"[INIT] Python: {sys.version}", file=sys.stderr)
print(f"[INIT] CWD: {os.getcwd()}", file=sys.stderr)

app = Flask(__name__)

# 測試 yfinance 導入
try:
    import yfinance as yf
    print(f"[OK] yfinance imported: {yf.__version__}", file=sys.stderr)
except Exception as e:
    print(f"[ERROR] yfinance import failed: {e}", file=sys.stderr)
    yf = None

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
    """獲取股票數據"""
    global yf
    if yf is None:
        print("[ERROR] yfinance not imported", file=sys.stderr)
        return {}
    
    data = {}
    for key, ticker in STOCK_TICKERS.items():
        try:
            print(f"[DEBUG] Fetching {key} ({ticker})...", file=sys.stderr)
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            print(f"[DEBUG] {key}: {len(hist)} rows", file=sys.stderr)
            
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
            else:
                print(f"[WARN] {key}: 無數據或數據不足", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] {key}: {type(e).__name__}: {e}", file=sys.stderr)
    
    return data

def get_fx_data():
    """獲取外匯數據"""
    global yf
    if yf is None:
        return {}
    
    data = {}
    for key, ticker in FX_TICKERS.items():
        try:
            print(f"[DEBUG] Fetching {key} ({ticker})...", file=sys.stderr)
            forex = yf.Ticker(ticker)
            hist = forex.history(period="5d")
            print(f"[DEBUG] {key}: {len(hist)} rows", file=sys.stderr)
            
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
            else:
                print(f"[WARN] {key}: 無數據或數據不足", file=sys.stderr)
        except Exception as e:
            print(f"[ERROR] {key}: {type(e).__name__}: {e}", file=sys.stderr)
    
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
        return jsonify({"error": "無法獲取股票數據", "debug": "檢查 PythonAnywhere 錯誤日誌"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    if not data:
        return jsonify({"error": "無法獲取外匯數據", "debug": "檢查 PythonAnywhere 錯誤日誌"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api", "data_source": "yfinance"})

@app.route('/debug')
def debug():
    global yf
    results = {
        "python_version": sys.version,
        "yfinance_imported": yf is not None,
        "test_results": {}
    }
    
    if yf is not None:
        for ticker in ["^HSI", "HKDUSD=X", "^DJI"]:
            try:
                t = yf.Ticker(ticker)
                h = t.history(period="5d")
                results["test_results"][ticker] = {
                    "rows": len(h),
                    "columns": list(h.columns) if not h.empty else [],
                    "last_price": float(h['Close'].iloc[-1]) if not h.empty and len(h) > 0 else None,
                    "last_date": str(h.index[-1]) if not h.empty and len(h) > 0 else None
                }
            except Exception as e:
                results["test_results"][ticker] = {"error": f"{type(e).__name__}: {e}"}
    else:
        results["error"] = "yfinance not imported"
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v3.3", "data_source": "yfinance", "no_fallback": True})

application = app
