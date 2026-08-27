# 快速修復指南 - 硬編碼數據

## 問題
API 返回空 `{}`，可能是 yfinance 未安裝或網絡問題。

## 立即解決方案（使用硬編碼數據）

### 步驟 1: 在 PythonAnywhere Bash 控制台執行

```bash
# 進入目錄
cd /home/chanpuirider/szcb-market-api

# 拉取最新代碼
git pull

# 替換 wsgi.py（使用硬編碼數據）
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

STOCK_DATA = {
    "hsi": {"price": 22500.50, "previous_close": 22230.00, "percent": 1.22},
    "dji": {"price": 38000.00, "previous_close": 37700.00, "percent": 0.80},
    "spx": {"price": 5200.00, "previous_close": 5175.00, "percent": 0.48},
    "ixic": {"price": 16500.00, "previous_close": 16350.00, "percent": 0.92},
    "sse": {"price": 3200.00, "previous_close": 3190.00, "percent": 0.31}
}

FX_DATA = {
    "usd": {"price": 7.82, "previous_close": 7.81, "percent": 0.13},
    "eur": {"price": 8.50, "previous_close": 8.48, "percent": 0.24},
    "gbp": {"price": 9.90, "previous_close": 9.88, "percent": 0.20},
    "jpy": {"price": 0.0521, "previous_close": 0.0520, "percent": 0.19},
    "cny": {"price": 1.07, "previous_close": 1.07, "percent": 0.00}
}

@app.route('/api/stocks')
def stocks():
    return jsonify(STOCK_DATA)

@app.route('/api/fx-rates')
def fx_rates():
    return jsonify(FX_DATA)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

application = app
ENDOFFILE

# 替換 PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'ENDOFFILE'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
ENDOFFILE

# 驗證
cat /var/www/chanpuirider_pythonanywhere_com_wsgi.py

# 測試
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates
```

### 步驟 2: 在 Web 頁面點擊 **Reload**

### 步驟 3: 測試市場頁面
http://localhost:9091/market.html

## 測試成功後

如果硬編碼數據可以工作，我們可以之後再添加 yfinance 來獲取實時數據。

## 如果需要恢復實時數據

執行以下命令啟用 yfinance：
```bash
cd /home/chanpuirider/szcb-market-api
source venv/bin/activate
pip install yfinance

# 然後編輯 wsgi.py，移除硬編碼數據，使用 yfinance
```
