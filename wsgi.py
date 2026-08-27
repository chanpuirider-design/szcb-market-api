import sys
import os
from flask import Flask, jsonify, make_response

APP_DIR = '/home/chanpuirider/szcb-market-api'
sys.path.insert(0, APP_DIR)
os.chdir(APP_DIR)

app = Flask(__name__)

# 使用多個替代 ticker 格式
STOCK_TICKERS = {
    "hsi": ["HSI:HK", "^HSI", "280005.HK"],
    "dji": ["DJI:IND", "^DJI", "DJIA"],
    "spx": ["SPX:IND", "^GSPC", "SPY"],
    "ixic": ["IXIC:IND", "^IXIC", "QQQ"],
    "sse": ["000001.SS", "SSE:000001", "SHCOMP"]
}

FX_TICKERS = {
    "usd": ["USDHKD=X", "HKDUSD=X", "USDHKD=F"],
    "eur": ["EURHKD=X", "HKDEUR=X"],
    "gbp": ["GBPHKD=X", "HKDGBP=X"],
    "jpy": ["JPYHKD=X", "HKDJPY=X"],
    "cny": ["CNHHKD=X", "HKDCNY=X"]
}

def get_data(ticker_list, is_fx=False):
    """嘗試多個 ticker 格式獲取數據"""
    try:
        import yfinance as yf
    except ImportError:
        return {}
    
    data = {}
    for key in ticker_list.keys():
        for ticker in ticker_list[key]:
            try:
                if is_fx:
                    # 外匯：嘗試正向和反向
                    tickers_to_try = [ticker, ticker.replace('X=', 'X=')[::-1].replace('X=', 'X=')[::-1] if '=' in ticker else None]
                    tickers_to_try = [t for t in tickers_to_try if t]
                else:
                    tickers_to_try = [ticker]
                
                for t in tickers_to_try:
                    try:
                        obj = yf.Ticker(t)
                        hist = obj.history(period="5d")
                        
                        if not hist.empty and len(hist) >= 2:
                            current = hist['Close'].iloc[-1]
                            prev_close = hist['Close'].iloc[-2]
                            percent = ((current - prev_close) / prev_close) * 100
                            
                            data[key] = {
                                "price": round(current, 2),
                                "previous_close": round(prev_close, 2),
                                "percent": round(percent, 2)
                            }
                            print(f"[OK] {key} via {t}: {current}", file=sys.stderr)
                            break
                    except Exception as e:
                        print(f"[WARN] {key} ({t}): {e}", file=sys.stderr)
                
                if key in data:
                    break
            except Exception as e:
                print(f"[ERROR] {key} ({ticker}): {e}", file=sys.stderr)
    
    return data

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/api/stocks')
def stocks():
    data = get_data(STOCK_TICKERS)
    if not data:
        return jsonify({"error": "無法獲取股票數據", "debug": "檢查 PythonAnywhere 網絡"}), 503
    return jsonify(data)

@app.route('/api/fx-rates')
def fx_rates():
    data = get_data(FX_TICKERS, is_fx=True)
    if not data:
        return jsonify({"error": "無法獲取外匯數據", "debug": "檢查 PythonAnywhere 網絡"}), 503
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "shcb-market-api"})

@app.route('/debug')
def debug():
    """調試端點"""
    try:
        import yfinance as yf
        results = {}
        
        # 測試不同的 ticker 格式
        test_cases = [
            ("^HSI", "恒生指數"),
            ("HSI:HK", "恒生指數 alt"),
            ("280005.HK", "恒指 ETF"),
            ("^DJI", "道瓊斯"),
            ("DJI:IND", "道瓊斯 alt"),
            ("^GSPC", "標普500"),
            ("SPY", "標普500 ETF"),
            ("^IXIC", "納斯達克"),
            ("QQQ", "納指 ETF"),
            ("000001.SS", "上证"),
            ("SHCOMP", "上证 alt"),
            ("USDHKD=X", "美元/港元"),
            ("USDHKD=X", "美元/港元 alt"),
            ("EURHKD=X", "歐元/港元"),
            ("GBPUSD=X", "英鎊/美元測試"),
        ]
        
        for ticker, name in test_cases:
            try:
                t = yf.Ticker(ticker)
                h = t.history(period="5d")
                results[ticker] = {
                    "name": name,
                    "rows": len(h),
                    "last_price": float(h['Close'].iloc[-1]) if not h.empty else None,
                    "columns": list(h.columns) if not h.empty else []
                }
            except Exception as e:
                results[ticker] = {"name": name, "error": str(e)}
        
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    return jsonify({"message": "SHCB Market Data API v4.0"})

application = app
