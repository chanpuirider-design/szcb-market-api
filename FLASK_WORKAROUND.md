# PythonAnywhere WSGI 修復 - Flask 包裝器方案

## 問題
FastAPI 是 ASGI 框架，PythonAnywhere 使用 WSGI。需要橋接。

## 解決方案

### 步驟 1: 安裝依賴
```bash
cd /home/chanpuirider/szcb-market-api
source venv/bin/activate
pip install flask
```

### 步驟 2: 創建 Flask 包裝器
```bash
cat > wsgi.py << 'EOF'
import sys
import os
from flask import Flask, request as flask_request

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 導入 FastAPI 應用
from main import app as fastapi_app

# 創建 Flask 應用
app = Flask(__name__)

# 簡單路由處理
@app.route('/api/stocks')
@app.route('/api/fx-rates')
@app.route('/health')
@app.route('/')
def handle_root():
    # 直接調用 FastAPI 應用
    from main import get_stock_data, get_fx_rates, health_check
    from flask import jsonify
    
    path = flask_request.path
    
    if path == '/api/stocks':
        data = get_stock_data()
        return jsonify(data)
    elif path == '/api/fx-rates':
        data = get_fx_rates()
        return jsonify(data)
    elif path == '/health':
        data = health_check()
        return jsonify(data)
    elif path == '/docs' or path == '/redoc':
        return "<html><body><h1>API Documentation</h1><p>Visit <a href='/docs'>/docs</a></p></body></html>"
    else:
        return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

# WSGI 入口
application = app
EOF
```

### 步驟 3: 更新 PythonAnywhere WSGI 文件
```bash
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os
from flask import Flask, request as flask_request

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from main import app as fastapi_app
from main import get_stock_data, get_fx_rates, health_check

app = Flask(__name__)

@app.route('/api/stocks')
@app.route('/api/fx-rates')
@app.route('/health')
@app.route('/')
def handle_root():
    path = flask_request.path
    
    if path == '/api/stocks':
        data = get_stock_data()
        return jsonify(data)
    elif path == '/api/fx-rates':
        data = get_fx_rates()
        return jsonify(data)
    elif path == '/health':
        data = health_check()
        return jsonify(data)
    else:
        return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

from flask import jsonify
application = app
EOF
```

### 步驟 4: 測試
```bash
python -c "from wsgi import application; print('✅ 成功!')"
```

### 步驟 5: 重啟
在 Web 頁面點擊 Reload
