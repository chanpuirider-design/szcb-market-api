# SHCB Market Data API

FastAPI-based market data API for SHCB Risk Analytics Team.
Deployed on Render.

## Features
- Stock indices (HSI, DJI, SPX, IXIC, SSE)
- FX rates (USD/HKD, EUR/HKD, GBP/HKD, JPY/HKD, CNY/HKD)
- Yahoo Finance integration via yfinance
- CORS enabled
- Auto-generated API documentation

## Endpoints
| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and endpoints |
| `GET /api/stocks` | Major stock indices |
| `GET /api/fx-rates` | FX rates |
| `GET /api/yahoo/ticker/{ticker}` | Specific ticker data |
| `GET /health` | Health check |

## API Documentation
- Swagger UI: https://your-app.onrender.com/docs
- ReDoc: https://your-app.onrender.com/redoc

## Local Development
```bash
cd fastapi_app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Deploy to Render

### Step 1: Create GitHub Repository
```bash
cd /c/Users/superuser01/hermes_web_page/szcb-team
git init fastapi_app
cd fastapi_app
git add .
git commit -m "Initial commit: SHCB Market Data API"
git remote add origin https://github.com/yourusername/szcb-market-api.git
git push -u origin main
```

### Step 2: Deploy on Render
1. 訪問 https://render.com/
2. 使用 GitHub 登錄
3. 點擊 "New +" → "Web Service"
4. 選擇倉庫 `szcb-market-api`
5. 配置：
   - **Name**: `szcb-market-api`
   - **Root Directory**: `fastapi_app`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. 點擊 "Create Web Service"

### Step 3: Access API
- API URL: https://szcb-market-api.onrender.com
- Docs: https://szcb-market-api.onrender.com/docs

## Test Endpoints
```bash
# Stocks
curl https://szcb-market-api.onrender.com/api/stocks

# FX Rates
curl https://szcb-market-api.onrender.com/api/fx-rates

# Specific Ticker
curl https://szcb-market-api.onrender.com/api/yahoo/ticker/HSI
```
