from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import yfinance as yf
from datetime import datetime, timedelta
import os
import requests
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Import strategy API endpoints
from strategy_api import app as strategy_app
from manual_backtest_api import app as manual_backtest_app
from beta_application_api import router as beta_application_router

# Include strategy API routes
app.include_router(strategy_app.router, prefix="/api")
app.include_router(manual_backtest_app.router, prefix="/api")
app.include_router(beta_application_router, prefix="/api")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Mind2Profit API is running!"}

@app.get("/api/backtest")
def backtest(symbol: str = Query(..., description="Market symbol, e.g. NQ or ES")):
    # Map user-friendly symbols to Yahoo Finance tickers
    symbol_map = {
        "NQ": "NQ=F",
        "ES": "ES=F"
    }
    yf_symbol = symbol_map.get(symbol.upper())
    if not yf_symbol:
        return {"error": "Unsupported symbol. Use NQ or ES."}

    # Fetch last 90 days of daily data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    data = yf.download(yf_symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval="1d")

    if data.empty:
        return {"error": "No data found for symbol."}

    # Placeholder stats using real data
    closes = data['Close']
    pnl = float(closes.iloc[-1] - closes.iloc[0])
    win_rate = 0.5  # Placeholder
    avg_rr = 2.0    # Placeholder
    drawdown = float(closes.max() - closes.min())

    return {
        "symbol": symbol,
        "win_rate": win_rate,
        "avg_rr": avg_rr,
        "pnl": pnl,
        "drawdown": drawdown,
        "start": str(start_date.date()),
        "end": str(end_date.date()),
        "data_points": len(data)
    }

@app.get("/api/economic-data")
def economic_data():
    """
    Fetch latest US CPI data from FRED.
    """
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    if not FRED_API_KEY:
        return {"error": "FRED API key not set. Please set FRED_API_KEY in your environment."}
    # US CPI series ID: CPIAUCSL
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={FRED_API_KEY}&file_type=json"
    resp = requests.get(url)
    if resp.status_code != 200:
        return {"error": "Failed to fetch data from FRED."}
    data = resp.json()
    if "observations" not in data or not data["observations"]:
        return {"error": "No data returned from FRED."}
    latest = data["observations"][-1]
    return {
        "series_id": "CPIAUCSL",
        "title": "Consumer Price Index for All Urban Consumers: All Items (CPI-U)",
        "date": latest["date"],
        "value": latest["value"]
    }

@app.get("/api/economic-calendar")
def economic_calendar():
    """
    Fetch upcoming economic events from Trading Economics.
    """
    TE_API_KEY = os.getenv("TRADING_ECONOMICS_API_KEY")
    if not TE_API_KEY:
        return {"error": "Trading Economics API key not set. Please set TRADING_ECONOMICS_API_KEY in your environment."}
    url = f"https://api.tradingeconomics.com/calendar?c={TE_API_KEY}&f=json"
    resp = requests.get(url)
    if resp.status_code != 200:
        return {"error": "Failed to fetch data from Trading Economics."}
    data = resp.json()
    # Simplify and filter for upcoming high-impact events (limit to next 7 days, high impact)
    from datetime import datetime, timedelta
    now = datetime.utcnow()
    in_7_days = now + timedelta(days=7)
    events = []
    for event in data:
        # Parse date and filter for next 7 days
        try:
            event_date = datetime.strptime(event.get("Date", ""), "%Y-%m-%dT%H:%M:%S")
        except Exception:
            continue
        if not (now <= event_date <= in_7_days):
            continue
        # Only include high impact events
        if event.get("Importance") != "High":
            continue
        events.append({
            "id": event.get("EventId", event.get("Event", "")),
            "title": event.get("Event", ""),
            "date": event_date.strftime("%b %d"),
            "time": event_date.strftime("%H:%M"),
            "currency": event.get("Country", ""),
            "impact": "high",
            "actual": event.get("Actual"),
            "forecast": event.get("Forecast"),
            "previous": event.get("Previous"),
        })
    return {"events": events} 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
