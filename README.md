# SHCB Market Data API

FastAPI-based market data API for SHCB Risk Analytics Team.
Powered by Yahoo Finance via yfinance.

## Features
- Stock indices (HSI, DJI, SPX, IXIC, SSE)
- FX rates (USD/HKD, EUR/HKD, GBP/HKD, JPY/HKD, CNY/HKD)
- Single ticker queries
- CORS enabled
- Auto-generated API documentation

## Endpoints
- `GET /` - API info
- `GET /api/stocks` - Major stock indices
- `GET /api/fx-rates` - FX rates
- `GET /api/yahoo/ticker/{ticker}` - Specific ticker data
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Deploy to Fly.io (Free Tier)
```bash
# Install Fly CLI
# Windows: https://fly.io/docs/getting-started/installing-flyctl/
# Mac: brew install fly
# Linux: curl -L https://fly.io/install.sh | sh

# Login to Fly
fly auth login

# Initialize app
fly launch --no-deploy

# Deploy
fly deploy
```

## Deploy to Railway
1. Visit https://railway.app/
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `chanpuirider-design/szcb-market-api`
5. Set Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## API Documentation
- Swagger UI: https://your-app.fly.dev/docs
- ReDoc: https://your-app.fly.dev/redoc

## Test Endpoints
```bash
# Stocks
curl https://your-app.fly.dev/api/stocks

# FX Rates
curl https://your-app.fly.dev/api/fx-rates

# Specific Ticker
curl https://your-app.fly.dev/api/yahoo/ticker/HSI
```
