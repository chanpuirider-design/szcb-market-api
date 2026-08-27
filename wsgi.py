import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 硬編碼的備用數據
DEFAULT_STOCK_DATA = {
    "hsi": {"price": 22500.50, "previous_close": 22230.00, "percent": 1.22},
    "dji": {"price": 38000.00, "previous_close": 37700.00, "percent": 0.80},
    "spx": {"price": 5200.00, "previous_close": 5175.00, "percent": 0.48},
    "ixic": {"price": 16500.00, "previous_close": 16350.00, "percent": 0.92},
    "sse": {"price": 3200.00, "previous_close": 3190.00, "percent": 0.31}
}

DEFAULT_FX_DATA = {
    "usd": {"price": 7.82, "previous_close": 7.81, "percent": 0.13},
    "eur": {"price": 8.50, "previous_close": 8.48, "percent": 0.24},
    "gbp": {"price": 9.90, "previous_close": 9.88, "percent": 0.20},
    "jpy": {"price": 0.0521, "previous_close": 0.0520, "percent": 0.19},
    "cny": {"price": 1.07, "previous_close": 1.07, "percent": 0.00}
}

# 股票代碼映射
STOCK_TICKERS = {
    "hsi": "^HSI",      # 恒生指數
    "dji": "^DJI",      # 道瓊斯
    "spx": "^GSPC",     # 標普500
    "ixic": "^IXIC",    # 納斯達克
    "sse": "000001.SS"  # 上证指數
}

# 外匯代碼映射
FX_TICKERS = {
    "usd": "HKDUSD=X",   # 美元/港元 (反向)
    "eur": "HKDEUR=X",   # 歐元/港元 (反向)
    "gbp": "HKDGBP=X",   # 英鎊/港元 (反向)
    "jpy": "HKDJPY=X",   # 日元/港元 (反向)
    "cny": "HKDCNY=X"    # 人民幣/港元 (反向)
}

def get_stock_data():
    """獲取股票數據，如果失敗則使用備用數據"""
    try:
        import yfinance as yf
        
        data = {}
        for key, ticker in STOCK_TICKERS.items():
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else hist['Close'].iloc[-1] * 0.99
                    percent_change = ((current - prev_close) / prev_close) * 100
                    
                    data[key] = {
                        "price": round(current, 2),
                        "previous_close": round(prev_close, 2),
                        "percent": round(percent_change, 2)
                    }
                else:
                    data[key] = DEFAULT_STOCK_DATA.get(key, {})
            except Exception as e:
                data[key] = DEFAULT_STOCK_DATA.get(key, {})
        
        return data if data else DEFAULT_STOCK_DATA
    except ImportError:
        return DEFAULT_STOCK_DATA
    except Exception:
        return DEFAULT_STOCK_DATA

def get_fx_data():
    """獲取外匯數據，如果失敗則使用備用數據"""
    try:
        import yfinance as yf
        
        data = {}
        for key, ticker in FX_TICKERS.items():
            try:
                forex = yf.Ticker(ticker)
                hist = forex.history(period="1d")
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current * 0.999
                    
                    # 計算百分比變化
                    percent_change = ((current - prev_close) / prev_close) * 100
                    
                    data[key] = {
                        "price": round(current, 4),
                        "previous_close": round(prev_close, 4),
                        "percent": round(percent_change, 2)
                    }
                else:
                    data[key] = DEFAULT_FX_DATA.get(key, {})
            except Exception as e:
                data[key] = DEFAULT_FX_DATA.get(key, {})
        
        return data if data else DEFAULT_FX_DATA
    except ImportError:
        return DEFAULT_FX_DATA
    except Exception:
        return DEFAULT_FX_DATA

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/stocks')
def stocks():
    data = get_stock_data()
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response

@app.route('/api/fx-rates')
def fx_rates():
    data = get_fx_data()
    response = make_response(jsonify(data))
    response.headers['Content-Type'] = 'application/json;charset=utf-8'
    return response

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API", "version": "2.0.0", "data_source": "yfinance"})

application = app
