from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
from beta_application_api import router as beta_application_router
from supabase_api import insert_waitlist_email, get_waitlist_emails

# Include strategy API routes
app.include_router(strategy_app.router, prefix="/api")
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

@app.get("/api/trading-topics")
def trading_topics():
    """
    Get comprehensive trading topics and educational content.
    """
    topics = {
        "fundamental_analysis": {
            "title": "Fundamental Analysis",
            "description": "Learn to analyze company financials, economic indicators, and market conditions",
            "topics": [
                "Financial Statement Analysis",
                "Economic Indicators (GDP, CPI, Employment)",
                "Industry Analysis",
                "Company Valuation Methods",
                "Earnings Reports and Guidance"
            ],
            "difficulty": "Intermediate",
            "estimated_time": "4-6 weeks"
        },
        "technical_analysis": {
            "title": "Technical Analysis",
            "description": "Master chart patterns, indicators, and price action analysis",
            "topics": [
                "Chart Patterns (Head & Shoulders, Triangles)",
                "Support and Resistance Levels",
                "Moving Averages and Trend Analysis",
                "RSI, MACD, and Other Indicators",
                "Volume Analysis and Price Action"
            ],
            "difficulty": "Beginner to Advanced",
            "estimated_time": "3-5 weeks"
        },
        "risk_management": {
            "title": "Risk Management",
            "description": "Essential strategies to protect your capital and maximize returns",
            "topics": [
                "Position Sizing and Money Management",
                "Stop Loss and Take Profit Strategies",
                "Risk-Reward Ratios",
                "Portfolio Diversification",
                "Emotional Control and Psychology"
            ],
            "difficulty": "All Levels",
            "estimated_time": "2-3 weeks"
        },
        "options_trading": {
            "title": "Options Trading",
            "description": "Advanced strategies using options for hedging and speculation",
            "topics": [
                "Options Basics (Calls and Puts)",
                "Option Greeks (Delta, Gamma, Theta, Vega)",
                "Covered Calls and Protective Puts",
                "Iron Condors and Butterflies",
                "Options for Income Generation"
            ],
            "difficulty": "Advanced",
            "estimated_time": "6-8 weeks"
        },
        "futures_trading": {
            "title": "Futures Trading",
            "description": "Trading futures contracts for commodities, indices, and currencies",
            "topics": [
                "Futures Contract Basics",
                "Margin Requirements and Leverage",
                "Commodity Trading (Oil, Gold, Corn)",
                "Index Futures (ES, NQ, YM)",
                "Futures for Hedging"
            ],
            "difficulty": "Intermediate to Advanced",
            "estimated_time": "4-6 weeks"
        },
        "day_trading": {
            "title": "Day Trading",
            "description": "Intraday trading strategies and techniques",
            "topics": [
                "Day Trading Setup and Requirements",
                "Scalping and Momentum Trading",
                "Breakout and Breakdown Strategies",
                "Market Opening and Closing Strategies",
                "Risk Management for Day Trading"
            ],
            "difficulty": "Intermediate to Advanced",
            "estimated_time": "3-4 weeks"
        },
        "swing_trading": {
            "title": "Swing Trading",
            "description": "Medium-term trading strategies holding positions for days to weeks",
            "topics": [
                "Swing Trading vs Day Trading",
                "Trend Following Strategies",
                "Mean Reversion Strategies",
                "Entry and Exit Timing",
                "Managing Swing Positions"
            ],
            "difficulty": "Intermediate",
            "estimated_time": "3-4 weeks"
        },
        "psychology": {
            "title": "Trading Psychology",
            "description": "Master the mental aspects of trading for consistent success",
            "topics": [
                "Emotional Control and Discipline",
                "Fear and Greed Management",
                "Trading Journal and Self-Analysis",
                "Building Confidence and Consistency",
                "Overcoming Trading Biases"
            ],
            "difficulty": "All Levels",
            "estimated_time": "Ongoing"
        }
    }
    
    return {
        "message": "Trading Topics and Educational Content",
        "total_topics": len(topics),
        "topics": topics,
        "recommended_order": [
            "risk_management",
            "technical_analysis", 
            "fundamental_analysis",
            "psychology",
            "swing_trading",
            "day_trading",
            "futures_trading",
            "options_trading"
        ]
    }

from pydantic import BaseModel

class WaitlistRequest(BaseModel):
    email: str

@app.post("/api/waitlist")
def add_to_waitlist(request: WaitlistRequest):
    """
    Add an email to the waitlist
    """
    try:
        email = request.email
        if not email or not "@" in email:
            return {"error": "Valid email is required"}
        
        # Insert into Supabase
        result = insert_waitlist_email(email)
        
        if result:
            return {
                "success": True,
                "message": "Successfully added to waitlist",
                "email": email
            }
        else:
            return {"error": "Failed to add to waitlist"}
            
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}

@app.get("/api/waitlist")
def get_waitlist():
    """
    Get all waitlist emails (admin only)
    """
    try:
        emails = get_waitlist_emails()
        return {
            "success": True,
            "count": len(emails),
            "emails": emails
        }
    except Exception as e:
        return {"error": f"Server error: {str(e)}"}

@app.get("/admin/waitlist")
def waitlist_admin():
    """
    Serve the waitlist admin page
    """
    try:
        with open("waitlist_admin.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return {"error": "Admin page not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
