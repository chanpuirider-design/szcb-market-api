import sys
import os
from flask import Flask, jsonify

# 配置應用目錄
APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

# 創建 Flask 應用
app = Flask(__name__)

# 簡單路由 - 不依賴 main.py
@app.route('/api/stocks')
def stocks():
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
                        'price': close,
                        'previous_close': prev_close,
                        'percent': round(((close - prev_close) / prev_close) * 100, 2) if prev_close else 0
                    }
            except Exception as e:
                result[name.lower()] = {'error': str(e)}
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fx-rates')
def fx_rates():
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
                        'price': close,
                        'previous_close': prev_close,
                        'percent': round(((close - prev_close) / prev_close) * 100, 4) if prev_close else 0
                    }
            except Exception as e:
                result[name.lower()] = {'error': str(e)}
        
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
        "endpoints": [
            "/api/stocks",
            "/api/fx-rates",
            "/health"
        ]
    })

# WSGI 入口
application = app
