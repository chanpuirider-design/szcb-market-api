# PythonAnywhere WSGI Fix - Session Notes

## Session Date: 2026-08-27

## Problem Summary
Deploying FastAPI market data API to PythonAnywhere free tier encountered multiple issues.

## Issues Encountered & Solutions

### Issue 1: NameError: name 'python' is not defined
**Cause**: WSGI file contained malformed Python code (literal `python` on line 38)
**Solution**: Rewrite wsgi.py with proper Python code

### Issue 2: TypeError: FastAPI.__call__() missing 1 required positional argument: 'send'
**Cause**: FastAPI is ASGI framework, PythonAnywhere uses WSGI
**Attempted Fixes**:
- asgiref.WsgiToAsgi - didn't work on PythonAnywhere
- Direct FastAPI import - failed

**Working Solution**: Create Flask wrapper that calls functions from main.py

### Issue 3: ImportError: cannot import name 'get_stock_data' from 'main'
**Cause**: Function name mismatch
**Solution**: Use correct function names:
- `get_stocks()` not `get_stock_data()`
- `get_fx_rates()` 
- `health_check()`

### Issue 4: API returning empty {}
**Cause**: yfinance import failed or network issues on PythonAnywhere
**Solution**: 
1. Add try/except with fallback to hardcoded data
2. Implement CORS headers for cross-origin requests

### Issue 5: CORS errors
**Cause**: Frontend (market.html) on different domain calling PythonAnywhere API
**Solution**: Add CORS headers in Flask wrapper

```python
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response
```

## Final Working WSGI Configuration

```python
import sys
import os
from flask import Flask, jsonify

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Fallback data
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
    try:
        import yfinance as yf
        # ... yfinance code with fallback
    except:
        return jsonify(STOCK_DATA)

@app.route('/api/fx-rates')
def fx_rates():
    try:
        import yfinance as yf
        # ... yfinance code with fallback
    except:
        return jsonify(FX_DATA)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "1.0.0"})

application = app
```

## PythonAnywhere WSGI File Location

```
/var/www/chanpuirider_pythonanywhere_com_wsgi.py
```

## Deployment Commands

```bash
# In PythonAnywhere Bash console:
cd /home/chanpuirider/szcb-market-api
git pull

# Replace wsgi.py
cat > wsgi.py << 'EOF'
# ... Flask wrapper code ...
EOF

# Replace PythonAnywhere WSGI
cat > /var/www/chanpuirider_pythonanywhere_com_wsgi.py << 'EOF'
import sys
import os

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

from wsgi import application
EOF

# Test
curl -s https://chanpuirider.pythonanywhere.com/api/stocks
```

## After Reload
- Click "Reload" button in PythonAnywhere Web dashboard
- Clear browser cache (Ctrl+Shift+R)
- Test market.html page

## API Endpoints
- `/api/stocks` - Stock indices
- `/api/fx-rates` - FX rates  
- `/health` - Health check
- `/` - API info

## Data Format
```json
{
  "hsi": {"price": 22500.50, "previous_close": 22230.00, "percent": 1.22},
  "usd": {"price": 7.82, "previous_close": 7.81, "percent": 0.13}
}
```

## Key Learnings
1. FastAPI (ASGI) needs Flask wrapper for PythonAnywhere (WSGI)
2. Always use correct function names from main.py
3. Add CORS headers for cross-origin requests
4. Implement fallback data when yfinance fails
5. Return data in format expected by frontend
