# 部署詳細日誌版本

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 拉取最新代碼
cd /home/chanpuirider/szcb-market-api
git pull

# 2. 激活虛擬環境
source venv/bin/activate

# 3. 替換 wsgi.py
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

print(f"[INIT] APP_DIR: {APP_DIR}", file=sys.stderr)
print(f"[INIT] Python: {sys.version}", file=sys.stderr)
print(f"[INIT] CWD: {os.getcwd()}", file=sys.stderr)

app = Flask(__name__)

try:
    import yfinance as yf
    print(f"[OK] yfinance imported: {yf.__version__}", file=sys.stderr)
except Exception as e:
    print(f"[ERROR] yfinance import failed: {e}", file=sys.stderr)
    yf = None

STOCK_TICKERS = {
    "hsi": "^HSI",
    "dji": "^DJI",
    "spx": "^GSPC",
    "ixic": "^IXIC",
    "sse": "000001.SS"
}

FX_TICKERS = {
    "usd": "HKDUSD=X",
    "eur": "HKDEUR=X",
    "gbp": "HKDGBP=X",
    "jpy": "HKDJPY=X",
    "cny": "HKDCNY=X"
}

def get_stock_data():
    global yf
    if yf is None:
        return {}
    data = {}
    for key, ticker in STOCK_TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent = ((current - prev_close) / prev_close) * 100
                data[key] = {"price": round(current, 2), "previous_close": round(prev_close, 2), "percent": round(percent, 2)}
        except Exception as e:
            print(f"[ERROR] {key}: {e}", file=sys.stderr)
    return data

def get_fx_data():
    global yf
    if yf is None:
        return {}
    data = {}
    for key, ticker in FX_TICKERS.items():
        try:
            forex = yf.Ticker(ticker)
            hist = forex.history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev_close = hist['Close'].iloc[-2]
                percent = ((current - prev_close) / prev_close) * 100
                data[key] = {"price": round(current, 4), "previous_close": round(prev_close, 4), "percent": round(percent, 2)}
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
                    "last_price": float(h['Close'].iloc[-1]) if not h.empty else None
                }
            except Exception as e:
                results["test_results"][ticker] = {"error": str(e)}
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v3.3"})

application = app
ENDOFFILE

# 4. 替換 PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'ENDOFFILE'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
ENDOFFILE

# 5. 測試
curl -s https://chanpuirider.pythonanywhere.com/debug
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 檢查 **PythonAnywhere 錯誤日誌**（看到 [ERROR] 或 [OK] 訊息）
3. 測試：http://localhost:9091/market.html
