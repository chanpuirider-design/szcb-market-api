"""SHCB Market Data API - FastAPI + Yahoo Finance (Render)"""

import urllib.request
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yfinance as yf

app = FastAPI(
    title="SHCB Market Data API",
    description="Stock and FX market data API for SHCB RA Team",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "SHCB Market Data API - Render Deployment",
        "endpoints": {
            "/api/stocks": "Get major stock indices",
            "/api/fx-rates": "Get FX rates",
            "/api/yahoo/ticker/{ticker}": "Get specific ticker data"
        },
        "status": "running"
    }

@app.get("/api/stocks")
async def get_stocks():
    """Get major stock indices from Yahoo Finance"""
    try:
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
                print(f"Error fetching {name}: {e}")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/fx-rates")
async def get_fx_rates():
    """Get FX rates from Yahoo Finance"""
    try:
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
                print(f"Error fetching {name}: {e}")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/yahoo/ticker/{ticker}")
async def get_yahoo_data(ticker: str):
    """Get specific ticker data from Yahoo Finance"""
    try:
        # Format ticker if needed
        if not ticker.startswith('^') and not ticker.endswith('=X'):
            if ticker in ['HSI', 'DJI', 'SPX', 'IXIC', 'HSTECH', 'HSCEI']:
                ticker = '^' + ticker
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="Ticker not found")
        
        meta = stock.info
        close = float(hist['Close'].iloc[-1])
        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else close
        
        return {
            'ticker': ticker,
            'price': close,
            'change': round(close - prev_close, 2),
            'change_percent': round(((close - prev_close) / prev_close) * 100, 2) if prev_close else 0,
            'previous_close': prev_close,
            'currency': meta.get('currency', 'USD'),
            'name': meta.get('shortName', ticker)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "shcb-market-api"}

if __name__ == '__main__':
    import uvicorn
    import os
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)
