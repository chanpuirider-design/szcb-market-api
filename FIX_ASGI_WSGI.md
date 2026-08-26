# PythonAnywhere ASGI 修復指南

## 問題
FastAPI 是 ASGI 框架，但 PythonAnywhere 使用 WSGI。需要轉換。

## 解決方案

### 步驟 1: 在 Bash 控制台執行

```bash
# 進入應用目錄
cd /home/chanpuirider/szcb-market-api

# 安裝 asgiref（WSGI/ASGI 轉換器）
source venv/bin/activate
pip install asgiref

# 替換 wsgi.py
cat > wsgi.py << 'EOF'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from main import app

# 使用 asgiref 轉換 ASGI 到 WSGI
from asgiref.wsgi import WsgiToAsgi
application = WsgiToAsgi(app)
EOF

# 驗證
cat wsgi.py

# 測試導入
python -c "from wsgi import application; print('✅ WSGI 應用創建成功!')"
```

### 步驟 2: 更新 PythonAnywhere 的 WSGI 文件

```bash
# 替換 PythonAnywhere 的 WSGI 文件
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from main import app
from asgiref.wsgi import WsgiToAsgi
application = WsgiToAsgi(app)
EOF

# 驗證
cat /var/www/chanpuirider_pythonanywhere_com_wsgi.py
```

### 步驟 3: 重啟

1. 在 **Web** 頁面點擊 **Reload**
2. 等待 30 秒
3. 測試：`curl https://chanpuirider.pythonanywhere.com/api/stocks`

---

## 備用方案：創建 Flask 包裝器

如果上面的方法不行，可以創建一個 Flask 應用來包裝 FastAPI：

```bash
# 安裝 Flask
pip install flask

# 創建 Flask 包裝器
cat > wsgi.py << 'EOF'
import sys
import os
from flask import Flask, Response, request as flask_request

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 導入 FastAPI 應用
from main import fastapi_app

# 註冊路由
for route in fastapi_app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        @app.route(route.path, methods=list(route.methods))
        def make_handler(route=route):
            async def handler(**kwargs):
                # 調用 FastAPI 路由
                from starlette.routing import Match
                match, scope, params = route.matches(flask_request.environ)
                if match == Match.FULL:
                    # 調用 FastAPI 處理函數
                    return await route.endpoint(**params)
            return handler
EOF
```

但通常第一個方案（asgiref）就足夠了。
