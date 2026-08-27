# 部署版本 8 - 修復 WSGI 路徑

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 首先確認虛擬環境 Python 路徑
which python3
ls -la /home/chanpuirider/szcb-market-api/venv/bin/python3
ls -la /home/chanpuirider/szcb-market-api/venv/bin/python

# 2. 拉取最新代碼
cd /home/chanpuirider/szcb-market-api
git pull

# 3. 激活虛擬環境
source venv/bin/activate

# 4. 替換 wsgi.py
cat > wsgi.py << 'ENDOFFILE'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

print(f"[INIT] Python: {sys.executable}", file=sys.stderr)
print(f"[INIT] Version: {sys.version}", file=sys.stderr)
print(f"[INIT] Path: {sys.path}", file=sys.stderr)

try:
    import yfinance as yf
    print(f"[OK] yfinance {yf.__version__} from: {yf.__file__}", file=sys.stderr)
except Exception as e:
    print(f"[ERROR] yfinance import failed: {e}", file=sys.stderr)
    yf = None

from flask import Flask, jsonify, make_response

app = Flask(__name__)

STOCK_TICKERS = {"hsi": "^HSI", "dji": "^DJI", "spx": "^GSPC", "ixic": "^IXIC", "sse": "000001.SS"}
FX_TICKERS = {"usd": "USDHKD=X", "eur": "EURHKD=X", "gbp": "GBPUSD=X", "jpy": "JPYHKD=X", "cny": "CNHHKD=X"}

def get_stock_data():
    global yf
    if yf is None: return {}
    data = {}
    for key, ticker in STOCK_TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="5d", timeout=30)
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
    if yf is None: return {}
    data = {}
    for key, ticker in FX_TICKERS.items():
        try:
            forex = yf.Ticker(ticker)
            hist = forex.history(period="5d", timeout=30)
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
    if not data: return jsonify({"error": "無法獲取股票數據"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    if not data: return jsonify({"error": "無法獲取外匯數據"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/debug')
def debug():
    global yf
    results = {
        "python_executable": sys.executable,
        "python_version": sys.version,
        "yfinance_imported": yf is not None,
        "yfinance_path": getattr(yf, '__file__', 'unknown'),
        "test_results": {}
    }
    if yf is not None:
        for ticker in ["^HSI", "USDHKD=X", "^DJI"]:
            try:
                t = yf.Ticker(ticker)
                h = t.history(period="5d", timeout=30)
                results["test_results"][ticker] = {"rows": len(h), "last_price": float(h['Close'].iloc[-1]) if not h.empty else None}
            except Exception as e:
                results["test_results"][ticker] = {"error": str(e)}
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v4.4"})

application = app
ENDOFFILE

# 5. 替換 PythonAnywhere WSGI - 使用正確的虛擬環境 Python
# 先找到虛擬環境 Python 的正確路徑
VENV_PYTHON=$(which python3)
echo "虛擬環境 Python: $VENV_PYTHON"

cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << ENDOFFILE
${VENV_PYTHON}
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
ENDOFFILE

# 6. 檢查 WSGI 文件
echo "=== WSGI 文件內容 ==="
head -5 /var/www/chanpuirider_pythonanywhere_com_wsgi.py
echo ""
echo "=== 權限 ==="
ls -la /var/www/chanpuirider_pythonanywhere_com_wsgi.py

# 7. 測試
curl -s https://chanpuirider.pythonanywhere.com/debug
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html

## 注意：
- 如果 shebang 仍然不工作，請在 PythonAnywhere Web 頁面檢查設定
- 可能需要設置 **WSGI Configuration File** 為 `/home/chanpuirider/szcb-market-api/wsgi.py`
