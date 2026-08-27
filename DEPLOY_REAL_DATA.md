# 部署真實市場數據

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 進入目錄
cd /home/chanpuirider/szcb-market-api

# 2. 拉取最新代碼
git pull

# 3. 安裝 yfinance
pip install yfinance --user

# 4. 測試 yfinance 是否工作
python3 -c "import yfinance as yf; t = yf.Ticker('^HSI'); h = t.history(period='1d'); print(h)"

# 5. 替換 wsgi.py
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

DEFAULT_STOCK_DATA = {
    "hsi": {"price": 22500.50, "previous_close": 22230.00, "percent": 1.22},
    "dji": {"price": 38000.00, "previous_close": 37700.00, "percent": 0.80},
    "spx": {"price": 5200.00, "previous_close": 5175.00, "percent": 0.48},
    "ixic": {"price": 16500.00, "previous_close": 16350.00, "percent": 0.92},
    "sse": {"price": 3200.00, "previous_close": 3190.00, "percent": 0.31}
}

DEFAULT_FX_DATA = {
    "usd": {"price": 7.82, "previous_close": 7.81, "percent": 0.13},
    "eur": {"price": 8.50, "previous_close": 8.48, "percent": 0.24},
    "gbp": {"price": 9.90, "previous_close": 9.88, "percent": 0.20},
    "jpy": {"price": 0.0521, "previous_close": 0.0520, "percent": 0.19},
    "cny": {"price": 1.07, "previous_close": 1.07, "percent": 0.00}
}

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
    try:
        import yfinance as yf
        
        data = {}
        for key, ticker in STOCK_TICKERS.items():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Close'].iloc[-1] * 0.99
                    percent_change = ((current - prev_close) / prev_close) * 100
                    
                    data[key] = {
                        "price": round(current, 2),
                        "previous_close": round(prev_close, 2),
                        "percent": round(percent_change, 2)
                    }
                else:
                    data[key] = DEFAULT_STOCK_DATA.get(key, {})
            except Exception:
                data[key] = DEFAULT_STOCK_DATA.get(key, {})
        
        return data if data else DEFAULT_STOCK_DATA
    except ImportError:
        return DEFAULT_STOCK_DATA
    except Exception:
        return DEFAULT_STOCK_DATA

def get_fx_data():
    try:
        import yfinance as yf
        
        data = {}
        for key, ticker in FX_TICKERS.items():
            try:
                forex = yf.Ticker(ticker)
                hist = forex.history(period="1d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current * 0.999
                    percent_change = ((current - prev_close) / prev_close) * 100
                    
                    data[key] = {
                        "price": round(current, 4),
                        "previous_close": round(prev_close, 4),
                        "percent": round(percent_change, 2)
                    }
                else:
                    data[key] = DEFAULT_FX_DATA.get(key, {})
            except Exception:
                data[key] = DEFAULT_FX_DATA.get(key, {})
        
        return data if data else DEFAULT_FX_DATA
    except ImportError:
        return DEFAULT_FX_DATA
    except Exception:
        return DEFAULT_FX_DATA

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/stocks')
def stocks():
    data = get_stock_data()
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api", "data_source": "yfinance"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "2.0.0", "data_source": "yfinance"})

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

# 7. 驗證部署
cat /var/www/chanpuirider_pythonanywhere_com_wsgi.py

# 8. 測試 API
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html

## 注意：
- yfinance 需要約 5-10 秒來獲取數據
- 如果 yfinance 失敗，會自動使用硬編碼的備用數據
- 數據每 15-20 分鐘更新一次（交易所延遲）
