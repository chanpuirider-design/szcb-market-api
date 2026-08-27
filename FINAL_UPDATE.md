# PythonAnywhere 完整更新指令

## 請在 PythonAnywhere Bash 控制台執行：

```bash
# 1. 進入目錄
cd /home/chanpuirider/szcb-market-api

# 2. 拉取最新代碼
git pull

# 3. 替換 wsgi.py（添加 CORS 支持）
cat > wsgi.py << 'ENDOFFILE'
import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 添加 CORS 頭
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

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

# 4. 替換 PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'ENDOFFILE'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
ENDOFFILE

# 5. 驗證
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
curl -s https://chanpuirider.pythonanywhere.com/api/fx-rates

# 6. 測試 CORS
curl -s -H "Origin: http://localhost:9091" https://chanpuirider.pythonanywhere.com/api/stocks -I
```

## 然後：
1. 在 **Web** 頁面點擊 **Reload**
2. 清除瀏覽器緩存（Ctrl+Shift+R）
3. 測試市場頁面：http://localhost:9091/market.html

## 預期結果
- 市場數據應該顯示
- 沒有 CORS 錯誤
- 滾動字幕應該更新
