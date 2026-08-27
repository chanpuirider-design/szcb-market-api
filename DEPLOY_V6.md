# 部署版本 4 - 多種 ticker 格式

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
    "hsi": ["HSI:HK", "^HSI", "280005.HK"],
    "dji": ["DJI:IND", "^DJI", "DJIA"],
    "spx": ["SPX:IND", "^GSPC", "SPY"],
    "ixic": ["IXIC:IND", "^IXIC", "QQQ"],
    "sse": ["000001.SS", "SSE:000001", "SHCOMP"]
}

FX_TICKERS = {
    "usd": ["USDHKD=X", "USDHKD=X", "HKDUSD=X"],
    "eur": ["EURHKD=X", "HKDEUR=X"],
    "gbp": ["GBPUSD=X", "GBPHKD=X"],
    "jpy": ["JPYHKD=X", "HKDJPY=X"],
    "cny": ["CNHHKD=X", "HKDCNY=X"]
}

def get_data(ticker_list, is_fx=False):
    try:
        import yfinance as yf
    except ImportError:
        return {}
    
    data = {}
    for key in ticker_list.keys():
        for ticker in ticker_list[key]:
            try:
                obj = yf.Ticker(ticker)
                hist = obj.history(period="5d")
                
                if not hist.empty and len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2]
                    percent = ((current - prev_close) / prev_close) * 100
                    
                    data[key] = {
                        "price": round(current, 2),
                        "previous_close": round(prev_close, 2),
                        "percent": round(percent, 2)
                    }
                    print(f"[OK] {key} via {ticker}: {current}", file=sys.stderr)
                    break
            except Exception as e:
                print(f"[WARN] {key} ({ticker}): {e}", file=sys.stderr)
    
    return data

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/stocks')
def stocks():
    data = get_data(STOCK_TICKERS)
    if not data:
        return jsonify({"error": "無法獲取股票數據"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_data(FX_TICKERS, is_fx=True)
    if not data:
        return jsonify({"error": "無法獲取外匯數據"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/debug')
def debug():
    try:
        import yfinance as yf
        results = {}
        test_cases = [
            ("HSI:HK", "恒生"),
            ("^HSI", "恒生^"),
            ("280005.HK", "恒指ETF"),
            ("^DJI", "道瓊斯"),
            ("DJI:IND", "道瓊斯alt"),
            ("^GSPC", "標普"),
            ("SPY", "標普ETF"),
            ("^IXIC", "納指"),
            ("QQQ", "納指ETF"),
            ("000001.SS", "上证"),
            ("SHCOMP", "上证alt"),
            ("USDHKD=X", "美元/港元"),
            ("USDHKD=X", "美元/港元alt"),
            ("EURHKD=X", "歐元/港元"),
            ("GBPUSD=X", "英鎊/美元"),
        ]
        
        for ticker, name in test_cases:
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
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v4.0"})

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
curl -s https://chanpuirider.pythonanywhere.com/debug | python3 -m json.tool
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 測試：http://localhost:9091/market.html
