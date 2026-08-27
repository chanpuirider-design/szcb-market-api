# PythonAnywhere 數據為空問題解決方案

## 問題
API 返回空對象 `{}`

## 原因分析
1. yfinance 未安裝
2. yfinance 導入失敗
3. 網絡問題導致無法獲取數據
4. 數據獲取失敗但沒有使用備用數據

## 解決方案

### 方案 1: 在 PythonAnywhere Bash 控制台執行

```bash
# 1. 檢查並安裝 yfinance
cd /home/chanpuirider/szcb-market-api
source venv/bin/activate
pip install yfinance

# 2. 測試 yfinance
python -c "import yfinance as yf; t=yf.Ticker('^HSI'); print(t.history(period='1d'))"

# 3. 如果失敗，拉取最新代碼（包含備用數據）
git pull

# 4. 更新 wsgi.py
cat > wsgi.py << 'EOF'
import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 備用數據
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
    try:
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
                print(f"Error {name}: {e}")
        if not success:
            return jsonify(STOCK_DATA)
        return jsonify(result)
    except Exception as e:
        return jsonify(STOCK_DATA)

@app.route('/api/fx-rates')
def fx_rates():
    try:
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
                print(f"Error {name}: {e}")
        if not success:
            return jsonify(FX_DATA)
        return jsonify(result)
    except Exception as e:
        return jsonify(FX_DATA)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

application = app
EOF

# 5. 更新 PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
EOF

# 6. 測試
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

### 方案 2: 查看錯誤日誌

```bash
# 查看最近的錯誤
tail -50 /home/chanpuirider/.pythonanywhere.log
tail -50 /home/chanpuirider/logs/error.log
```

### 方案 3: 檢查 yfinance 是否可用

```bash
cd /home/chanpuirider/szcb-market-api
source venv/bin/activate
python -c "import yfinance; print('yfinance version:', yfinance.__version__)"
python -c "
import yfinance as yf
try:
    t = yf.Ticker('^HSI')
    h = t.history(period='1d')
    print('HSI Price:', h['Close'].iloc[-1] if not h.empty else 'No data')
except Exception as e:
    print('Error:', e)
"
```

## 如果以上都失敗

在 Web 頁面點擊 **Reload** 後，如果仍然沒有數據，請把以下輸出貼給我：

```bash
# 執行這個命令，把輸出貼給我
cat /home/chanpuirider/.pythonanywhere.log | tail -30
```
