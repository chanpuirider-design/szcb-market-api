# PythonAnywhere API 更新指令

## 步驟 1: 在 Bash 控制台執行

```bash
# 進入應用目錄
cd /home/chanpuirider/szcb-market-api

# 拉取最新代碼
git pull

# 替換 wsgi.py
cat > wsgi.py << 'EOF'
"""
SHCB Market Data API - PythonAnywhere WSGI 配置
返回與 market.html 兼容的數據格式
"""
import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

@app.route('/api/stocks')
def stocks():
    """獲取股票指數數據"""
    try:
        import yfinance as yf
        
        tickers = {
            'HSI': '^HSI',
            'DJI': '^DJI',
            'SPX': '^GSPC',
            'IXIC': '^IXIC',
            'SSE': '000001.SS'
        }
        
        result = {}
        for name, ticker in tickers.items():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                
                if not hist.empty:
                    close = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else close
                    
                    result[name.lower()] = {
                        'price': round(close, 2),
                        'previous_close': round(prev_close, 2),
                        'percent': round(((close - prev_close) / prev_close) * 100, 2) if prev_close else 0
                    }
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fx-rates')
def fx_rates():
    """獲取外匯匯率數據"""
    try:
        import yfinance as yf
        
        currencies = {
            'USD': 'USDHKD=X',
            'EUR': 'EURHKD=X',
            'GBP': 'GBPHKD=X',
            'JPY': 'JPYHKD=X',
            'CNY': 'CNYHKD=X'
        }
        
        result = {}
        for name, ticker in currencies.items():
            try:
                pair = yf.Ticker(ticker)
                hist = pair.history(period="1d")
                
                if not hist.empty:
                    close = float(hist['Close'].iloc[-1])
                    prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else close
                    
                    result[name.lower()] = {
                        'price': round(close, 2),
                        'previous_close': round(prev_close, 2),
                        'percent': round(((close - prev_close) / prev_close) * 100, 2) if prev_close else 0
                    }
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "shcb-market-api"
    })

@app.route('/')
@app.route('/docs')
@app.route('/redoc')
def index():
    return jsonify({
        "message": "SHCB Market Data API",
        "version": "1.0.0",
        "endpoints": ["/api/stocks", "/api/fx-rates", "/health"]
    })

application = app
EOF

# 替換 PythonAnywhere 的 WSGI 文件
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
EOF

# 驗證
cat /var/www/chanpuirider_pythonanywhere_com_wsgi.py

# 測試
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

## 步驟 2: 在 Web 頁面點擊 Reload

## 步驟 3: 測試市場頁面
http://localhost:9091/market.html
或
https://dropout-poet-angler.ngrok-free.dev/market.html
