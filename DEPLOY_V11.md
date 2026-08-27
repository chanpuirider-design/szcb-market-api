# 部署版本 9 - 直接使用 Yahoo Finance API

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 拉取最新代碼
cd /home/chanpuirider/szcb-market-api
git pull

# 2. 激活虛擬環境
source venv/bin/activate

# 3. 替換 wsgi.py（不使用 yfinance，直接使用 Yahoo API）
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
import json
import time
import urllib.request
import urllib.error
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

def fetch_yahoo_data(symbol):
    """直接使用 Yahoo Finance API 獲取數據"""
    try:
        # 計算時間戳
        now = int(time.time())
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={now-172800}&period2={now}&interval=1d"
        
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
                closes = result['indicators']['quote'][0]['close']
                closes = [c for c in closes if c is not None]
                
                if len(closes) >= 2:
                    current = closes[-1]
                    prev_close = closes[-2]
                    percent = ((current - prev_close) / prev_close) * 100
                    return {
                        "price": round(current, 2),
                        "previous_close": round(prev_close, 2),
                        "percent": round(percent, 2)
                    }
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}", file=sys.stderr)
    
    return None

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
    "cny": "CNYHKD=X"
}

def get_stock_data():
    data = {}
    for key, symbol in STOCK_TICKERS.items():
        result = fetch_yahoo_data(symbol)
        if result:
            data[key] = result
            print(f"[OK] {key}: {result['price']}", file=sys.stderr)
    return data

def get_fx_data():
    data = {}
    for key, symbol in FX_TICKERS.items():
        result = fetch_yahoo_data(symbol)
        if result:
            data[key] = result
            print(f"[OK] {key}: {result['price']}", file=sys.stderr)
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
    results = {"python_version": sys.version, "test_results": {}}
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
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html

## 注意：
- 此版本不使用 yfinance，直接使用 Yahoo Finance API
- 如果仍然失敗，可能是 PythonAnywhere 網絡限制
