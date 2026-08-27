# 部署實時數據（無備用數據）

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 進入目錄
cd /home/chanpuirider/szcb-market-api

# 2. 拉取最新代碼
git pull

# 3. 激活虛擬環境
source venv/bin/activate

# 4. 安裝 yfinance（不使用 --user）
pip install yfinance

# 5. 測試 yfinance 是否正常
python3 -c "import yfinance as yf; t = yf.Ticker('^HSI'); h = t.history(period='1d'); print(h)"

# 6. 替換 wsgi.py
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

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
                data[key] = {"price": round(current, 2), "previous_close": round(prev_close, 2), "percent": round(percent, 2)}
        except:
            pass
    return data

def get_fx_data():
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
                data[key] = {"price": round(current, 4), "previous_close": round(prev_close, 4), "percent": round(percent, 2)}
        except:
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
ENDOFFILE

# 7. 替換 PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'ENDOFFILE'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
ENDOFFILE

# 8. 測試
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html

## 注意：
- 首次加載可能需要 10-20 秒
- 如果 yfinance 失敗，API 會返回 503 錯誤
- 市場休市時數據可能為空
