# 部署與調試

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
    errors = []
    
    for key, ticker in STOCK_TICKERS.items():
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            
            if hist.empty:
                errors.append(f"{key}: 無數據")
                continue
                
            if len(hist) < 2:
                errors.append(f"{key}: 數據不足")
                continue
            
            current = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            percent = ((current - prev_close) / prev_close) * 100
            
            data[key] = {
                "price": round(current, 2),
                "previous_close": round(prev_close, 2),
                "percent": round(percent, 2)
            }
        except Exception as e:
            errors.append(f"{key}: {str(e)}")
    
    if errors:
        print(f"[DEBUG] Stock Errors: {errors}", file=sys.stderr)
    
    return data

def get_fx_data():
    import yfinance as yf
    data = {}
    errors = []
    
    for key, ticker in FX_TICKERS.items():
        try:
            forex = yf.Ticker(ticker)
            hist = forex.history(period="2d")
            
            if hist.empty:
                errors.append(f"{key}: 無數據")
                continue
                
            if len(hist) < 2:
                errors.append(f"{key}: 數據不足")
                continue
            
            current = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2]
            percent = ((current - prev_close) / prev_close) * 100
            
            data[key] = {
                "price": round(current, 4),
                "previous_close": round(prev_close, 4),
                "percent": round(percent, 2)
            }
        except Exception as e:
            errors.append(f"{key}: {str(e)}")
    
    if errors:
        print(f"[DEBUG] FX Errors: {errors}", file=sys.stderr)
    
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
        return jsonify({"error": "無法獲取股票數據", "debug": "檢查日誌"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    if not data:
        return jsonify({"error": "無法獲取外匯數據", "debug": "檢查日誌"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api", "data_source": "yfinance"})

@app.route('/debug')
def debug():
    import yfinance as yf
    results = {}
    
    try:
        t = yf.Ticker("^HSI")
        h = t.history(period="2d")
        results["HSI_test"] = {
            "has_data": not h.empty,
            "rows": len(h),
            "columns": list(h.columns),
            "last_price": float(h['Close'].iloc[-1]) if not h.empty else None
        }
    except Exception as e:
        results["HSI_test"] = {"error": str(e)}
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v3.0", "data_source": "yfinance", "no_fallback": True})

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

# 5. 測試 debug 端點
curl -s https://chanpuirider.pythonanywhere.com/debug

# 6. 測試股票 API
curl -s https://chanpuirider.pythonanywhere.com/api/stocks

# 7. 測試外匯 API
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html
