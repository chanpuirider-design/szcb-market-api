import sys
import os
from flask import Flask, jsonify, make_response
import traceback

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

print(f"[START] Python: {sys.version}", file=sys.stderr)
print(f"[START] CWD: {os.getcwd()}", file=sys.stderr)
print(f"[START] PATH: {os.environ.get('PATH', 'N/A')}", file=sys.stderr)

# 嘗試導入 yfinance
try:
    import yfinance as yf
    print(f"[OK] yfinance imported: {yf.__version__}", file=sys.stderr)
except Exception as e:
    print(f"[ERROR] yfinance import failed: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    yf = None

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
    global yf
    if yf is None:
        print("[ERROR] yfinance not available", file=sys.stderr)
        return {}
    
    data = {}
    for key, ticker in STOCK_TICKERS.items():
        try:
            print(f"[DEBUG] Fetching {key} ({ticker})...", file=sys.stderr)
            stock = yf.Ticker(ticker)
            print(f"[DEBUG] Ticker object created for {ticker}", file=sys.stderr)
            
            # 使用 timeout 參數
            hist = stock.history(period="5d", timeout=30)
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
            traceback.print_exc(file=sys.stderr)
    
    return data

def get_fx_data():
    """獲取外匯數據"""
    global yf
    if yf is None:
        return {}
    
    data = {}
    for key, ticker in FX_TICKERS.items():
        try:
            print(f"[DEBUG] Fetching FX {key} ({ticker})...", file=sys.stderr)
            forex = yf.Ticker(ticker)
            hist = forex.history(period="5d", timeout=30)
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
            traceback.print_exc(file=sys.stderr)
    
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
        return jsonify({"error": "無法獲取股票數據", "debug": "查看錯誤日誌"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    if not data:
        return jsonify({"error": "無法獲取外匯數據", "debug": "查看錯誤日誌"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/debug')
def debug():
    global yf
    results = {
        "python_version": sys.version,
        "yfinance_imported": yf is not None,
        "yfinance_version": getattr(yf, '__version__', 'unknown') if yf else None,
        "test_results": {}
    }
    
    if yf is not None:
        for ticker in ["^HSI", "USDHKD=X", "^DJI"]:
            try:
                print(f"[DEBUG] Testing {ticker}...", file=sys.stderr)
                t = yf.Ticker(ticker)
                print(f"[DEBUG] Ticker created for {ticker}", file=sys.stderr)
                h = t.history(period="5d", timeout=30)
                print(f"[DEBUG] {ticker}: {len(h)} rows", file=sys.stderr)
                results["test_results"][ticker] = {
                    "rows": len(h),
                    "last_price": float(h['Close'].iloc[-1]) if not h.empty else None,
                    "error": None
                }
            except Exception as e:
                print(f"[ERROR] Test {ticker}: {type(e).__name__}: {e}", file=sys.stderr)
                traceback.print_exc(file=sys.stderr)
                results["test_results"][ticker] = {
                    "rows": 0,
                    "last_price": None,
                    "error": f"{type(e).__name__}: {str(e)}"
                }
    else:
        results["error"] = "yfinance not imported"
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v4.2", "data_source": "yfinance"})

application = app
