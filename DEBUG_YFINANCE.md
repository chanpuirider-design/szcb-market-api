# PythonAnywhere yfinance 錯誤修復指南

## 問題
API 返回空對象 `{}`，可能是因為 yfinance 沒有正確安裝或網絡問題。

## 解決方案

### 步驟 1: 檢查 yfinance 是否安裝
```bash
cd /home/chanpuirider/szcb-market-api
source venv/bin/activate
pip list | grep yfinance
```

如果沒有安裝，執行：
```bash
pip install yfinance
```

### 步驟 2: 測試 yfinance
```bash
python -c "
import yfinance as yf
t = yf.Ticker('^HSI')
h = t.history(period='1d')
print(h)
print('Price:', h['Close'].iloc[-1] if not h.empty else 'No data')
"
```

### 步驟 3: 查看錯誤日誌
```bash
tail -50 /home/chanpuirider/.pythonanywhere.log
tail -50 /home/chanpuirider/logs/error.log
```

### 步驟 4: 如果 yfinance 失敗，使用備用方案

編輯 wsgi.py，使用簡單的硬編碼數據作為備用：
```bash
cat > /home/chanpuirider/szcb-market-api/wsgi.py << 'EOF'
import sys
import os
from flask import Flask, jsonify
import random
from datetime import datetime

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 備用數據（當 yfinance 失敗時使用）
STOCK_DATA = {
    'hsi': {'price': 22500.50, 'previous_close': 22230.00, 'percent': 1.22},
    'dji': {'price': 38000.00, 'previous_close': 37700.00, 'percent': 0.80},
    'spx': {'price': 5200.00, 'previous_close': 5175.00, 'percent': 0.48},
    'ixic': {'price': 16500.00, 'previous_close': 16350.00, 'percent': 0.92},
    'sse': {'price': 3200.00, 'previous_close': 3190.00, 'percent': 0.31}
}

FX_DATA = {
    'usd': {'price': 7.82, 'previous_close': 7.81, 'percent': 0.13},
    'eur': {'price': 8.50, 'previous_close': 8.48, 'percent': 0.24},
    'gbp': {'price': 9.90, 'previous_close': 9.88, 'percent': 0.20},
    'jpy': {'price': 0.0521, 'previous_close': 0.0520, 'percent': 0.19},
    'cny': {'price': 1.07, 'previous_close': 1.07, 'percent': 0.00}
}

@app.route('/api/stocks')
def stocks():
    """獲取股票指數數據"""
    try:
        # 嘗試使用 yfinance
        import yfinance as yf
        tickers = {'HSI': '^HSI', 'DJI': '^DJI', 'SPX': '^GSPC', 'IXIC': '^IXIC', 'SSE': '000001.SS'}
        result = {}
        success = False
        
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
                    success = True
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        
        # 如果 yfinance 失敗，使用備用數據
        if not success:
            print("Using fallback data")
            return jsonify(STOCK_DATA)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in stocks: {e}")
        return jsonify(STOCK_DATA)

@app.route('/api/fx-rates')
def fx_rates():
    """獲取外匯匯率數據"""
    try:
        # 嘗試使用 yfinance
        import yfinance as yf
        currencies = {'USD': 'USDHKD=X', 'EUR': 'EURHKD=X', 'GBP': 'GBPHKD=X', 'JPY': 'JPYHKD=X', 'CNY': 'CNYHKD=X'}
        result = {}
        success = False
        
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
                    success = True
            except Exception as e:
                print(f"Error fetching {name}: {e}")
        
        # 如果 yfinance 失敗，使用備用數據
        if not success:
            print("Using fallback FX data")
            return jsonify(FX_DATA)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error in fx_rates: {e}")
        return jsonify(FX_DATA)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

application = app
EOF
```

### 步驟 5: 更新 PythonAnywhere WSGI
```bash
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
EOF
```

### 步驟 6: 重新載入
在 Web 頁面點擊 **Reload**

### 步驟 7: 測試
```bash
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```
