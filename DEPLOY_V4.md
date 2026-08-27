# 部署與調試 - 版本 2

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 進入目錄並拉取最新代碼
cd /home/chanpuirider/szcb-market-api
git pull

# 2. 激活虛擬環境
source venv/bin/activate

# 3. 安裝 yfinance
pip install yfinance

# 4. 測試 yfinance 是否能獲取數據
python3 << 'PYEOF'
import yfinance as yf
import datetime

print("測試 1: HSI 最近 10 天數據")
t = yf.Ticker("^HSI")
h = t.history(period="10d")
print(f"HSI: {len(h)} 行")
print(h.tail(3))

print("\n測試 2: 美元/港元")
f = yf.Ticker("HKDUSD=X")
fh = f.history(period="5d")
print(f"USD/HKD: {len(fh)} 行")
print(fh.tail(3))

print("\n測試 3: 道瓊斯")
d = yf.Ticker("^DJI")
dh = d.history(period="1d")
print(f"DJI: {len(dh)} 行")
print(dh.tail(1))
PYEOF

# 5. 替換 wsgi.py
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
from flask import Flask, jsonify, make_response
import datetime

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 嘗試多個 ticker 格式
STOCK_TICKERS = {
    "hsi": ["^HSI", "HK:HSI"],
    "dji": ["^DJI", "DJIA"],
    "spx": ["^GSPC", "SPX"],
    "ixic": ["^IXIC", "NASDAQ"],
    "sse": ["000001.SS", "SSE:000001"]
}

FX_TICKERS = {
    "usd": ["HKDUSD=X", "USDHKD=X"],
    "eur": ["HKDEUR=X", "EURHKD=X"],
    "gbp": ["HKDGBP=X", "GBPHKD=X"],
    "jpy": ["HKDJPY=X", "JPYHKD=X"],
    "cny": ["HKDCNY=X", "CNYHKD=X"]
}

def get_stock_data():
    import yfinance as yf
    data = {}
    
    for key, tickers in STOCK_TICKERS.items():
        for ticker in tickers:
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
                    print(f"[OK] {key} ({ticker}): {current}", file=sys.stderr)
                    break
                else:
                    print(f"[WARN] {key} ({ticker}): 無數據", file=sys.stderr)
            except Exception as e:
                print(f"[ERROR] {key} ({ticker}): {e}", file=sys.stderr)
    
    return data

def get_fx_data():
    import yfinance as yf
    data = {}
    
    for key, tickers in FX_TICKERS.items():
        for ticker in tickers:
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
                    print(f"[OK] {key} ({ticker}): {current}", file=sys.stderr)
                    break
                else:
                    print(f"[WARN] {key} ({ticker}): 無數據", file=sys.stderr)
            except Exception as e:
                print(f"[ERROR] {key} ({ticker}): {e}", file=sys.stderr)
    
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
        return jsonify({"error": "無法獲取股票數據", "debug": "檢查 PythonAnywhere 日誌"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    if not data:
        return jsonify({"error": "無法獲取外匯數據", "debug": "檢查 PythonAnywhere 日誌"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api", "data_source": "yfinance"})

@app.route('/debug')
def debug():
    import yfinance as yf
    results = {}
    
    # 測試多個 ticker
    test_tickers = ["^HSI", "HKDUSD=X", "^DJI", "NASDAQ"]
    for ticker in test_tickers:
        try:
            t = yf.Ticker(ticker)
            h = t.history(period="5d")
            results[ticker] = {
                "rows": len(h),
                "has_data": not h.empty,
                "columns": list(h.columns),
                "last_price": float(h['Close'].iloc[-1]) if not h.empty else None,
                "last_date": str(h.index[-1]) if not h.empty else None
            }
        except Exception as e:
            results[ticker] = {"error": str(e)}
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v3.1", "data_source": "yfinance", "no_fallback": True})

application = app
ENDOFFILE

# 6. 替換 PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'ENDOFFILE'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
ENDOFFILE

# 7. 測試
curl -s https://chanpuirider.pythonanywhere.com/debug
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html

## 注意：
- 如果所有 ticker 都失敗，可能是 PythonAnywhere 網絡問題
- 檢查 PythonAnywhere 的 Access/Error 日誌
