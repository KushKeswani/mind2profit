from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Optional, List, Dict, Any
import yfinance as yf
from datetime import datetime, timedelta, date
import os
from urllib.parse import quote
import requests
import json
import uuid
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv

# Always load backend/.env, not only when cwd is the backend folder
load_dotenv(Path(__file__).resolve().parent / ".env")

# Massive (https://massive.com) — economy endpoints use /fed/v1/...  (API key as query ?apiKey=)
MASSIVE_API_BASE = "https://api.massive.com"

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

def _massive_get(path: str, **params) -> Optional[dict]:
    """GET Massive REST API. Returns None if MASSIVE_API_KEY is unset. Raises no exceptions."""
    key = os.getenv("MASSIVE_API_KEY")
    if not key:
        return None
    q: Dict[str, Any] = {"apiKey": key}
    for k, v in params.items():
        if v is not None:
            q[k] = v
    try:
        r = requests.get(f"{MASSIVE_API_BASE}{path}", params=q, timeout=30)
    except Exception as exc:
        return {"status": "ERROR", "error": f"Massive request failed: {exc}"}
    try:
        data = r.json()
    except Exception:
        return {"status": "ERROR", "error": f"Invalid JSON from Massive (HTTP {r.status_code})"}
    if r.status_code != 200:
        if isinstance(data, dict) and data.get("error"):
            return data
        return {"status": "ERROR", "error": f"HTTP {r.status_code}"}
    if isinstance(data, dict) and data.get("status") not in (None, "OK"):
        return data
    return data


def _fmt_brief_date(iso_date: str) -> str:
    try:
        d = datetime.strptime(str(iso_date)[:10], "%Y-%m-%d")
        return d.strftime("%b %d")
    except Exception:
        return str(iso_date)[:10]


def _fred_cpi_latest() -> dict:
    """Latest CPI observation from FRED (fallback)."""
    fred = os.getenv("FRED_API_KEY")
    if not fred:
        return {"error": "FRED_API_KEY is not set."}
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={fred}&file_type=json"
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        return {"error": "Failed to fetch data from FRED."}
    data = resp.json()
    if "observations" not in data or not data["observations"]:
        return {"error": "No data returned from FRED."}
    latest = data["observations"][-1]
    return {
        "source": "fred",
        "series_id": "CPIAUCSL",
        "title": "Consumer Price Index for All Urban Consumers: All Items (CPI-U)",
        "date": latest["date"],
        "value": latest["value"],
    }


@app.get("/api/economic-data")
def economic_data():
    """
    Latest U.S. inflation snapshot. Prefers Massive `GET /fed/v1/inflation`, falls back to FRED CPI series.
    """
    massive = _massive_get("/fed/v1/inflation", limit="1", sort="date.desc")
    if massive is not None and massive.get("status") == "OK" and massive.get("results"):
        row = massive["results"][-1]
        cpi = row.get("cpi")
        yoy = row.get("cpi_year_over_year")
        pce = row.get("pce")
        pce_c = row.get("pce_core")
        value_parts: List[str] = []
        if cpi is not None:
            value_parts.append(f"CPI {cpi}")
        if yoy is not None:
            value_parts.append(f"CPI YoY {yoy}%")
        if pce is not None:
            value_parts.append(f"PCE {pce}")
        if pce_c is not None:
            value_parts.append(f"core PCE {pce_c}")
        return {
            "source": "massive",
            "series_id": "FED_INFLATION",
            "title": "U.S. realized inflation (CPI & PCE) — Massive",
            "date": row.get("date"),
            "value": " · ".join(value_parts) if value_parts else str(row),
        }

    fred = _fred_cpi_latest()
    if "error" not in fred:
        if massive is not None and massive.get("error"):
            fred["note"] = f"Fell back from Massive: {massive.get('error')}"
        elif massive is not None and massive.get("status") == "OK" and not massive.get("results"):
            fred["note"] = "Fell back from Massive: no rows returned."
        return fred

    return {
        "error": (massive.get("error") if massive and massive.get("error") else fred.get("error"))
        or "Set MASSIVE_API_KEY and/or FRED_API_KEY. See env_template.txt.",
    }


def _trading_economics_calendar() -> dict:
    te = os.getenv("TRADING_ECONOMICS_API_KEY")
    if not te:
        return {"error": "TRADING_ECONOMICS_API_KEY not set.", "events": []}
    url = f"https://api.tradingeconomics.com/calendar?c={te}&f=json"
    resp = requests.get(url, timeout=45)
    if resp.status_code != 200:
        return {"error": "Failed to fetch data from Trading Economics.", "events": []}
    data = resp.json()
    if not isinstance(data, list):
        return {"error": "Unexpected response from Trading Economics.", "events": []}
    now = datetime.utcnow()
    in_7_days = now + timedelta(days=7)
    events: List[Dict[str, Any]] = []
    for event in data:
        try:
            event_date = datetime.strptime(event.get("Date", ""), "%Y-%m-%dT%H:%M:%S")
        except Exception:
            continue
        if not (now <= event_date <= in_7_days):
            continue
        if event.get("Importance") != "High":
            continue
        events.append({
            "id": str(event.get("EventId", event.get("Event", ""))),
            "title": event.get("Event", ""),
            "date": event_date.strftime("%b %d"),
            "time": event_date.strftime("%H:%M"),
            "currency": str(event.get("Country", "")),
            "impact": "high",
            "actual": event.get("Actual"),
            "forecast": event.get("Forecast"),
            "previous": event.get("Previous"),
        })
    return {"source": "trading_economics", "events": events}


def _map_te_importance(imp: Any) -> str:
    if imp is None:
        return "low"
    if isinstance(imp, str):
        s = imp.strip().lower()
        if s in ("high", "h"):
            return "high"
        if s in ("medium", "med", "m"):
            return "medium"
        if s in ("low", "l"):
            return "low"
    try:
        n = int(float(imp))  # TE often uses 0, 1, 2
        if n >= 2:
            return "high"
        if n == 1:
            return "medium"
    except (TypeError, ValueError):
        pass
    return "low"


def _parse_te_datetime(s: str) -> Optional[datetime]:
    if not s or not isinstance(s, str):
        return None
    t = s.strip()
    if t.endswith("Z") and "T" in t:
        t = t[:-1]
    for fmt, chop in (("%Y-%m-%dT%H:%M:%S", 19), ("%Y-%m-%dT%H:%M:%S.%f", 26), ("%Y-%m-%d", 10)):
        try:
            return datetime.strptime(t[:chop] if len(t) >= chop else t, fmt)
        except (ValueError, TypeError, IndexError):
            continue
    return None


def _trading_economics_calendar_range(date_from: str, date_to: str) -> dict:
    """
    U.S. scheduled releases with all importance levels (red / orange / grey in the UI),
    in [date_from, date_to] inclusive, using the Trading Economics country+range endpoint.
    """
    te = os.getenv("TRADING_ECONOMICS_API_KEY")
    if not te:
        return {"error": "TRADING_ECONOMICS_API_KEY not set.", "events": []}
    d_from: date = datetime.strptime(date_from, "%Y-%m-%d").date()
    d_to: date = datetime.strptime(date_to, "%Y-%m-%d").date()
    if d_to < d_from:
        d_from, d_to = d_to, d_from
    day_span = (d_to - d_from).days
    if day_span > 120:
        return {"error": "Date range may not exceed 120 days.", "events": []}
    ctry = quote("united states", safe="")
    url = f"https://api.tradingeconomics.com/calendar/country/{ctry}/{date_from}/{date_to}?c={te}&f=json"
    try:
        resp = requests.get(url, timeout=60)
    except Exception as exc:  # noqa: BLE001
        return {"error": f"Trading Economics request failed: {exc}", "events": []}
    if resp.status_code != 200:
        return {"error": f"Failed to fetch calendar (HTTP {resp.status_code}).", "events": []}
    try:
        data = resp.json()
    except Exception:
        return {"error": "Invalid JSON from Trading Economics.", "events": []}
    if not isinstance(data, list):
        return {"error": "Unexpected response from Trading Economics.", "events": []}
    out: List[Dict[str, Any]] = []
    for event in data:
        raw = event.get("Date", "")
        if not raw:
            continue
        event_dt = _parse_te_datetime(str(raw))
        if not event_dt:
            continue
        if event_dt.tzinfo:
            event_dt = event_dt.replace(tzinfo=None)
        e_date = event_dt.date()
        if e_date < d_from or e_date > d_to:
            continue
        eid = event.get("CalendarId") or event.get("EventId", "")
        eid_s = str(eid).strip() if eid is not None else ""
        out.append(
            {
                "id": f"te-{eid_s or 'e'}-{e_date}",
                "title": str(event.get("Event", "") or event.get("Category", ""))[:200],
                "dateIso": e_date.isoformat(),
                "time": event_dt.strftime("%H:%M"),
                "datetime": str(event.get("Date", ""))[:32],
                "currency": str(event.get("Country", event.get("Currency", "")) or "USD")[:24],
                "country": str(event.get("Country", ""))[:80],
                "category": str(event.get("Category", ""))[:120],
                "impact": _map_te_importance(event.get("Importance")),
                "actual": event.get("Actual"),
                "forecast": event.get("Forecast") or event.get("TEForecast"),
                "previous": event.get("Previous"),
            }
        )
    out.sort(key=lambda e: (e.get("dateIso", ""), e.get("time", "")))
    return {"source": "trading_economics", "events": out}


def _massive_events_in_range(date_from: str, date_to: str) -> dict:
    if not os.getenv("MASSIVE_API_KEY"):
        return {"error": "MASSIVE_API_KEY not set.", "events": []}
    d_from = datetime.strptime(date_from, "%Y-%m-%d").date()
    d_to = datetime.strptime(date_to, "%Y-%m-%d").date()
    if d_to < d_from:
        d_from, d_to = d_to, d_from
    day_span = (d_to - d_from).days
    if day_span > 400:
        return {"error": "Date range for Massive is too large. Narrow the window.", "events": []}
    infl_raw = _massive_get("/fed/v1/inflation", limit="200", sort="date.desc")
    lab_raw = _massive_get("/fed/v1/labor-market", limit="200", sort="date.desc")
    exp_raw = _massive_get("/fed/v1/inflation-expectations", limit="200", sort="date.desc")
    yld_raw = _massive_get("/fed/v1/treasury-yields", limit="500", sort="date.desc")
    infl_rows = (infl_raw or {}).get("results") or [] if (infl_raw and infl_raw.get("status") == "OK") else []
    lab_rows = (lab_raw or {}).get("results") or [] if (lab_raw and lab_raw.get("status") == "OK") else []
    exp_rows = (exp_raw or {}).get("results") or [] if (exp_raw and exp_raw.get("status") == "OK") else []
    yld_rows = (yld_raw or {}).get("results") or [] if (yld_raw and yld_raw.get("status") == "OK") else []
    events: List[Dict[str, Any]] = []
    for row in infl_rows:
        if not isinstance(row, dict) or not row.get("date"):
            continue
        cpi = row.get("cpi")
        yoy = row.get("cpi_year_over_year")
        actual = " · ".join(
            s
            for s in [
                f"CPI {cpi}" if cpi is not None else "",
                f"CPI YoY {yoy}%" if yoy is not None else "",
            ]
            if s
        ) or str(row)
        d = str(row["date"])[:10]
        d_o = datetime.strptime(d, "%Y-%m-%d").date()
        if d_o < d_from or d_o > d_to:
            continue
        events.append(
            {
                "id": f"massive-infl-{d}",
                "title": "U.S. inflation: CPI, core, PCE (realized)",
                "dateIso": d,
                "time": "00:00",
                "currency": "USD",
                "country": "United States",
                "impact": "high",
                "actual": actual,
                "forecast": None,
                "previous": None,
            }
        )
    for row in lab_rows:
        if not isinstance(row, dict) or not row.get("date"):
            continue
        ur = row.get("unemployment_rate")
        ptc = row.get("labor_force_participation_rate")
        jm = row.get("job_openings")
        ahe = row.get("avg_hourly_earnings")
        actual = " · ".join(
            s
            for s in [
                f"UNRATE {ur}%" if ur is not None else "",
                f"participation {ptc}%" if ptc is not None else "",
                f"openings {jm}k" if jm is not None else "",
                f"avg hourly ${ahe}" if ahe is not None else "",
            ]
            if s
        ) or str(row)
        d = str(row["date"])[:10]
        d_o = datetime.strptime(d, "%Y-%m-%d").date()
        if d_o < d_from or d_o > d_to:
            continue
        events.append(
            {
                "id": f"massive-labor-{d}",
                "title": "U.S. labor market (FRED / Massive)",
                "dateIso": d,
                "time": "00:00",
                "currency": "USD",
                "country": "United States",
                "impact": "medium",
                "actual": actual,
                "forecast": None,
                "previous": None,
            }
        )
    for row in exp_rows:
        if not isinstance(row, dict) or not row.get("date"):
            continue
        m5 = row.get("market_5_year")
        m10 = row.get("market_10_year")
        mo1 = row.get("model_1_year")
        mo5 = row.get("model_5_year")
        actual = " · ".join(
            s
            for s in [
                f"5Y breakeven {m5}%" if m5 is not None else "",
                f"10Y breakeven {m10}%" if m10 is not None else "",
                f"model 1Y {mo1}%" if mo1 is not None else "",
                f"model 5Y {mo5}%" if mo5 is not None else "",
            ]
            if s
        ) or str(row)
        d = str(row["date"])[:10]
        d_o = datetime.strptime(d, "%Y-%m-%d").date()
        if d_o < d_from or d_o > d_to:
            continue
        events.append(
            {
                "id": f"massive-infl-exp-{d}",
                "title": "U.S. inflation expectations (breakevens, Cleveland Fed)",
                "dateIso": d,
                "time": "00:00",
                "currency": "USD",
                "country": "United States",
                "category": "Inflation expectations",
                "impact": "medium",
                "actual": actual,
                "forecast": None,
                "previous": None,
            }
        )
    # One Treasury snapshot per ISO week in range (avoids a separate row for every trading day)
    seen_treasury_weeks: set = set()
    for row in sorted(yld_rows, key=lambda r: str((r or {}).get("date", ""))):
        if not isinstance(row, dict) or not row.get("date"):
            continue
        d = str(row["date"])[:10]
        d_o = datetime.strptime(d, "%Y-%m-%d").date()
        if d_o < d_from or d_o > d_to:
            continue
        wk = d_o.isocalendar()[:2]
        if wk in seen_treasury_weeks:
            continue
        seen_treasury_weeks.add(wk)
        parts: List[str] = []
        for key, label in (
            ("yield_3_month", "3M"),
            ("yield_2_year", "2Y"),
            ("yield_5_year", "5Y"),
            ("yield_10_year", "10Y"),
            ("yield_30_year", "30Y"),
        ):
            v = row.get(key)
            if v is not None:
                parts.append(f"{label} {v}%")
        actual = " · ".join(parts) if parts else str(row)
        events.append(
            {
                "id": f"massive-ust-{d}",
                "title": "U.S. Treasury constant-maturity yields (week snapshot)",
                "dateIso": d,
                "time": "00:00",
                "currency": "USD",
                "country": "United States",
                "category": "Treasury yields",
                "impact": "low",
                "actual": actual,
                "forecast": None,
                "previous": None,
            }
        )
    events.sort(key=lambda e: e.get("dateIso", ""), reverse=True)
    if not events and infl_raw and infl_raw.get("error"):
        return {"error": str(infl_raw.get("error")), "events": []}
    if not events and lab_raw and lab_raw.get("error"):
        return {"error": str(lab_raw.get("error")), "events": []}
    return {"source": "massive", "events": events}


def _massive_macro_events() -> dict:
    """
    Real macro series from Massive (monthly FRED-based aggregates). Not a 'scheduled' calendar, but true data.
    """
    if not os.getenv("MASSIVE_API_KEY"):
        return {"error": "MASSIVE_API_KEY not set.", "events": []}
    infl_raw = _massive_get("/fed/v1/inflation", limit="6", sort="date.desc")
    labor_raw = _massive_get("/fed/v1/labor-market", limit="6", sort="date.desc")
    infl_rows = (infl_raw or {}).get("results") or [] if (infl_raw and infl_raw.get("status") == "OK") else []
    lab_rows = (labor_raw or {}).get("results") or [] if (labor_raw and labor_raw.get("status") == "OK") else []
    events: List[Dict[str, Any]] = []
    for row in infl_rows:
        if not isinstance(row, dict) or not row.get("date"):
            continue
        cpi = row.get("cpi")
        yoy = row.get("cpi_year_over_year")
        actual = " · ".join(
            s for s in [
                f"CPI {cpi}" if cpi is not None else "",
                f"CPI YoY {yoy}%" if yoy is not None else "",
            ] if s
        ) or str(row)
        d = str(row["date"])[:10]
        events.append({
            "_sort": d,
            "id": f"massive-infl-{d}",
            "title": "U.S. inflation: CPI, core, PCE (realized)",
            "date": _fmt_brief_date(d),
            "time": "—",
            "currency": "USD",
            "impact": "high",
            "actual": actual,
            "forecast": None,
            "previous": None,
        })
    for row in lab_rows:
        if not isinstance(row, dict) or not row.get("date"):
            continue
        ur = row.get("unemployment_rate")
        jm = row.get("job_openings")
        ptc = row.get("labor_force_participation_rate")
        ahe = row.get("avg_hourly_earnings")
        actual = " · ".join(
            s for s in [
                f"UNRATE {ur}%" if ur is not None else "",
                f"participation {ptc}%" if ptc is not None else "",
                f"openings {jm}k" if jm is not None else "",
                f"avg hourly ${ahe}" if ahe is not None else "",
            ] if s
        ) or str(row)
        d = str(row["date"])[:10]
        events.append({
            "_sort": d,
            "id": f"massive-labor-{d}",
            "title": "U.S. labor market (FRED / Massive)",
            "date": _fmt_brief_date(d),
            "time": "—",
            "currency": "USD",
            "impact": "high",
            "actual": actual,
            "forecast": None,
            "previous": None,
        })
    events.sort(key=lambda e: e.get("_sort", ""), reverse=True)
    for e in events:
        e.pop("_sort", None)
    if not events:
        emsg = (infl_raw or {}).get("error") or (labor_raw or {}).get("error") or "No rows returned (check MASSIVE_API_KEY / plan)."
        return {"error": str(emsg), "events": []}
    return {"source": "massive", "events": events[:12]}


@app.get("/api/economic-calendar/range")
def economic_calendar_range(
    dfrom: str = Query(..., alias="from", description="Window start (YYYY-MM-DD)"),
    dto: str = Query(..., alias="to", description="Window end (YYYY-MM-DD)"),
) -> dict:
    """
    Economic calendar for a custom date range (month, week, or day).

    When `TRADING_ECONOMICS_API_KEY` is set, returns the full U.S. release schedule (all impact levels) with
    actual / forecast / previous as provided. When `MASSIVE_API_KEY` is also set, appends FRED-based macro
    (inflation, labor, inflation expectations, weekly Treasury snapshot) for the same window so you can
    combine the news calendar with realized macro series. If only Massive is configured, all four Massive
    economy feeds are used for that range.
    """
    try:
        a = datetime.strptime(dfrom, "%Y-%m-%d").date()
        b = datetime.strptime(dto, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "from and to must be YYYY-MM-DD.", "events": []}
    d1, d2 = (dfrom, dto) if a <= b else (dto, dfrom)
    te_key = os.getenv("TRADING_ECONOMICS_API_KEY")
    m_key = os.getenv("MASSIVE_API_KEY")
    merged: List[Dict[str, Any]] = []
    sources: List[str] = []
    te_error: Optional[str] = None
    mass_error: Optional[str] = None
    te_ok = False
    m_result: Optional[dict] = None

    if te_key:
        r = _trading_economics_calendar_range(d1, d2)
        if r.get("error"):
            te_error = str(r.get("error") or "Trading Economics error")
        else:
            te_ok = True
            merged.extend(r.get("events") or [])
            sources.append("trading_economics")
    if m_key:
        m_result = _massive_events_in_range(d1, d2)
        if m_result.get("error"):
            mass_error = str(m_result.get("error") or "Massive error")
        m_events = m_result.get("events") or []
        if m_events:
            merged.extend(m_events)
            if "massive" not in sources:
                sources.append("massive")
    if merged:
        merged.sort(key=lambda e: (e.get("dateIso", ""), e.get("time", "")))
        out: Dict[str, Any] = {"source": "+".join(sources), "events": merged}
        if te_error and te_key:
            out["trading_economics_error"] = te_error
        if mass_error and m_key:
            out["massive_error"] = mass_error
        return out
    if te_ok:
        return {
            "source": "trading_economics" + ("+massive" if m_key else ""),
            "events": [],
            **({"massive_error": mass_error} if mass_error else {}),
        }
    if m_key and m_result and not m_result.get("error"):
        return {"source": m_result.get("source", "massive"), "events": []}
    if te_error and mass_error:
        return {
            "error": f"Trading Economics: {te_error}. Massive: {mass_error}.",
            "events": [],
        }
    if te_error:
        return {"error": te_error, "events": []}
    if mass_error:
        return {"error": mass_error, "events": []}
    return {
        "error": "Set TRADING_ECONOMICS_API_KEY and/or MASSIVE_API_KEY. See env_template.txt.",
        "events": [],
    }


@app.get("/api/economic-calendar")
def economic_calendar():
    """
    Prefer U.S. macro (Massive / FRED). If you also use Trading Economics, that runs as a fallback when Massive is empty.
    """
    if os.getenv("MASSIVE_API_KEY"):
        massive_cal = _massive_macro_events()
        if massive_cal.get("events"):
            return massive_cal
    if os.getenv("TRADING_ECONOMICS_API_KEY"):
        return _trading_economics_calendar()
    if os.getenv("MASSIVE_API_KEY"):
        return _massive_macro_events()
    return {
        "error": "Set MASSIVE_API_KEY and/or TRADING_ECONOMICS_API_KEY. See env_template.txt.",
        "events": [],
    }

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

from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOURNAL_FILE = os.path.join(BASE_DIR, "journal_entries.json")
TRADOVATE_CONNECTION_FILE = os.path.join(BASE_DIR, "tradovate_connection.json")
EMAIL_REMINDER_STATE_FILE = os.path.join(BASE_DIR, "email_reminder_state.json")
_email_scheduler_thread: Optional[threading.Thread] = None


class JournalTrade(BaseModel):
    symbol: str
    type: str
    entry: float
    exit: float
    pnl: float
    riskReward: str
    time: Optional[str] = ""


class JournalEntryRequest(BaseModel):
    date: str
    trades: List[JournalTrade]
    reflection: str
    tags: List[str] = Field(default_factory=list)
    good: Optional[str] = ""
    bad: Optional[str] = ""
    ugly: Optional[str] = ""
    goals: Optional[str] = ""


class TradeChatRequest(BaseModel):
    message: str


class TradovateConnectRequest(BaseModel):
    name: str
    password: str
    appId: str
    appVersion: str = "1.0"
    cid: str
    sec: str
    isDemo: bool = True


class TradovateTokenConnectRequest(BaseModel):
    accessToken: str
    isDemo: bool = True
    username: Optional[str] = "manual-token"


class LaunchAnnouncementRequest(BaseModel):
    subject: Optional[str] = "Mind2Profit is now LIVE - Opening Sale"
    ctaUrl: Optional[str] = None


def _read_journal_entries() -> List[Dict[str, Any]]:
    if not os.path.exists(JOURNAL_FILE):
        return []
    try:
        with open(JOURNAL_FILE, "r", encoding="utf-8") as journal_file:
            data = json.load(journal_file)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _write_journal_entries(entries: List[Dict[str, Any]]) -> None:
    with open(JOURNAL_FILE, "w", encoding="utf-8") as journal_file:
        json.dump(entries, journal_file, indent=2)


def _read_tradovate_connection() -> Optional[Dict[str, Any]]:
    if not os.path.exists(TRADOVATE_CONNECTION_FILE):
        return None
    try:
        with open(TRADOVATE_CONNECTION_FILE, "r", encoding="utf-8") as connection_file:
            data = json.load(connection_file)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return None


def _write_tradovate_connection(connection: Dict[str, Any]) -> None:
    with open(TRADOVATE_CONNECTION_FILE, "w", encoding="utf-8") as connection_file:
        json.dump(connection, connection_file, indent=2)


def _delete_tradovate_connection() -> None:
    if os.path.exists(TRADOVATE_CONNECTION_FILE):
        os.remove(TRADOVATE_CONNECTION_FILE)


def _read_email_reminder_state() -> Dict[str, Any]:
    if not os.path.exists(EMAIL_REMINDER_STATE_FILE):
        return {}
    try:
        with open(EMAIL_REMINDER_STATE_FILE, "r", encoding="utf-8") as reminder_file:
            data = json.load(reminder_file)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _write_email_reminder_state(state: Dict[str, Any]) -> None:
    with open(EMAIL_REMINDER_STATE_FILE, "w", encoding="utf-8") as reminder_file:
        json.dump(state, reminder_file, indent=2)


def _recent_trade_context(entries: List[Dict[str, Any]], max_entries: int = 8) -> str:
    if not entries:
        return "No trades logged yet."
    recent_entries = entries[-max_entries:]
    lines: List[str] = []
    for entry in recent_entries:
        date = entry.get("date", "unknown-date")
        reflection = entry.get("reflection", "")
        for trade in entry.get("trades", []):
            lines.append(
                f"{date} | {trade.get('symbol')} | {trade.get('type')} | "
                f"entry={trade.get('entry')} exit={trade.get('exit')} pnl={trade.get('pnl')} rr={trade.get('riskReward')}"
            )
        if reflection:
            lines.append(f"Reflection: {reflection}")
    return "\n".join(lines)


def _today_journal_entries() -> List[Dict[str, Any]]:
    today = datetime.now().date()
    entries = _read_journal_entries()
    todays_entries: List[Dict[str, Any]] = []
    for entry in entries:
        raw_date = entry.get("date")
        if not raw_date:
            continue
        try:
            entry_date = datetime.fromisoformat(raw_date).date()
        except Exception:
            try:
                entry_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
            except Exception:
                continue
        if entry_date == today:
            todays_entries.append(entry)
    return todays_entries


def _build_eod_email_html(entries: List[Dict[str, Any]], login_url: str) -> str:
    total_trades = 0
    wins = 0
    total_pnl = 0.0
    symbol_map: Dict[str, int] = {}

    for entry in entries:
        for trade in entry.get("trades", []):
            total_trades += 1
            pnl = float(trade.get("pnl", 0) or 0)
            total_pnl += pnl
            if pnl > 0:
                wins += 1
            symbol = str(trade.get("symbol", "UNKNOWN"))
            symbol_map[symbol] = symbol_map.get(symbol, 0) + 1

    win_rate = (wins / total_trades * 100) if total_trades else 0
    symbols_text = ", ".join([f"{symbol} ({count})" for symbol, count in symbol_map.items()]) or "No symbols logged"
    today_label = datetime.now().strftime("%A, %b %d, %Y")

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.5;">
        <h2>Mind2Profit End-of-Day Journal Reminder</h2>
        <p>Here is your trading summary for <strong>{today_label}</strong>.</p>
        <ul>
          <li><strong>Total trades:</strong> {total_trades}</li>
          <li><strong>Win rate:</strong> {win_rate:.1f}%</li>
          <li><strong>Total P&amp;L:</strong> {'+' if total_pnl >= 0 else ''}${total_pnl:,.2f}</li>
          <li><strong>Symbols traded:</strong> {symbols_text}</li>
          <li><strong>Journal entries created:</strong> {len(entries)}</li>
        </ul>
        <p>Take 3-5 minutes to reflect on your process, risk management, and discipline while the day is fresh.</p>
        <p>
          <a href="{login_url}" style="display:inline-block;padding:10px 16px;background:#2563eb;color:#fff;text-decoration:none;border-radius:6px;">
            Open Mind2Profit & Reflect
          </a>
        </p>
      </body>
    </html>
    """


def _send_eod_email_now() -> Dict[str, Any]:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipients_raw = os.getenv("DAILY_JOURNAL_REMINDER_EMAILS", "")
    recipients = [email.strip() for email in recipients_raw.split(",") if email.strip()]
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    login_url = os.getenv("MIND2PROFIT_LOGIN_URL", "http://localhost:8080")

    if not sender_email or not sender_password:
        return {"success": False, "error": "Missing SENDER_EMAIL or SENDER_PASSWORD."}
    if not recipients:
        return {"success": False, "error": "Set DAILY_JOURNAL_REMINDER_EMAILS in environment."}

    entries = _today_journal_entries()
    html = _build_eod_email_html(entries, login_url)

    message = MIMEMultipart("alternative")
    message["Subject"] = "Mind2Profit 5PM Journal Reminder"
    message["From"] = sender_email
    message["To"] = ", ".join(recipients)
    message.attach(MIMEText(html, "html"))

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipients, message.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipients, message.as_string())
        return {
            "success": True,
            "recipients": recipients,
            "entriesCount": len(entries),
            "sentAt": datetime.now().isoformat(),
        }
    except Exception as error:
        return {"success": False, "error": f"Failed to send email: {str(error)}"}


def _send_bulk_html_email(recipients: List[str], subject: str, html_body: str) -> Dict[str, Any]:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))

    if not sender_email or not sender_password:
        return {"success": False, "error": "Missing SENDER_EMAIL or SENDER_PASSWORD."}
    if not recipients:
        return {"success": False, "error": "No recipients provided."}

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = sender_email
    message["Bcc"] = ", ".join(recipients)
    message.attach(MIMEText(html_body, "html"))

    try:
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipients, message.as_string())
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as smtp:
                smtp.starttls()
                smtp.login(sender_email, sender_password)
                smtp.sendmail(sender_email, recipients, message.as_string())
        return {"success": True, "sentCount": len(recipients)}
    except Exception as error:
        return {"success": False, "error": f"Failed to send bulk email: {str(error)}"}


def _build_launch_announcement_html(cta_url: str) -> str:
    return f"""
    <html>
      <body style="margin:0;padding:0;background:#0b1020;font-family:Inter,Arial,sans-serif;color:#e5e7eb;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="padding:32px 16px;background:#0b1020;">
          <tr>
            <td align="center">
              <table role="presentation" width="620" cellspacing="0" cellpadding="0" style="max-width:620px;background:#111827;border:1px solid #1f2937;border-radius:14px;overflow:hidden;">
                <tr>
                  <td style="padding:28px 28px 16px 28px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);">
                    <p style="margin:0;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#dbeafe;">Mind2Profit Launch Update</p>
                    <h1 style="margin:10px 0 0 0;font-size:30px;line-height:1.2;color:#ffffff;">We are officially LIVE</h1>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px 28px;">
                    <p style="margin:0 0 14px 0;font-size:16px;line-height:1.6;color:#d1d5db;">
                      Thanks for joining the waitlist. Mind2Profit is now live and we are opening the doors to early users.
                    </p>
                    <div style="margin:18px 0;padding:14px 16px;border:1px solid #374151;border-radius:10px;background:#0f172a;">
                      <p style="margin:0;font-size:15px;line-height:1.6;color:#f9fafb;">
                        <strong>Special Opening Sale:</strong> Join now to lock in early pricing and get immediate access.
                      </p>
                    </div>
                    <p style="margin:22px 0 26px 0;">
                      <a href="{cta_url}" style="display:inline-block;padding:12px 20px;background:#2563eb;color:#ffffff;text-decoration:none;font-weight:600;border-radius:8px;">
                        Join Mind2Profit
                      </a>
                    </p>
                    <p style="margin:0 0 6px 0;font-size:13px;color:#9ca3af;">If the button does not work, copy this link:</p>
                    <p style="margin:0;font-size:13px;word-break:break-all;color:#93c5fd;">{cta_url}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """


def _daily_email_scheduler_loop() -> None:
    target_hour = int(os.getenv("DAILY_REMINDER_HOUR", "17"))
    target_minute = int(os.getenv("DAILY_REMINDER_MINUTE", "0"))
    while True:
        now = datetime.now()
        state = _read_email_reminder_state()
        today_key = now.strftime("%Y-%m-%d")
        already_sent_today = state.get("last_sent_date") == today_key

        if now.hour == target_hour and now.minute == target_minute and not already_sent_today:
            send_result = _send_eod_email_now()
            if send_result.get("success"):
                _write_email_reminder_state(
                    {
                        "last_sent_date": today_key,
                        "last_sent_at": send_result.get("sentAt"),
                        "last_result": "success",
                    }
                )
            else:
                _write_email_reminder_state(
                    {
                        "last_sent_date": state.get("last_sent_date"),
                        "last_sent_at": state.get("last_sent_at"),
                        "last_result": send_result.get("error", "failed"),
                    }
                )
        time.sleep(30)


def _tradovate_base_url(is_demo: bool) -> str:
    return "https://demo.tradovateapi.com/v1" if is_demo else "https://live.tradovateapi.com/v1"


def _tradovate_oauth_base_url(is_demo: bool) -> str:
    return "https://trader-demo.tradovate.com/oauth" if is_demo else "https://trader.tradovate.com/oauth"

class WaitlistRequest(BaseModel):
    email: str


@app.get("/api/journal/entries")
def get_journal_entries():
    entries = _read_journal_entries()
    return {"entries": entries}


@app.post("/api/journal/entries")
def create_journal_entry(request: JournalEntryRequest):
    entries = _read_journal_entries()
    new_entry = {
        "id": str(uuid.uuid4()),
        "date": request.date,
        "trades": [trade.dict() for trade in request.trades],
        "reflection": request.reflection,
        "tags": request.tags,
        "good": request.good,
        "bad": request.bad,
        "ugly": request.ugly,
        "goals": request.goals,
        "createdAt": datetime.utcnow().isoformat(),
    }
    entries.append(new_entry)
    _write_journal_entries(entries)
    return {"success": True, "entry": new_entry}


@app.put("/api/journal/entries/{entry_id}")
def update_journal_entry(entry_id: str, request: JournalEntryRequest):
    entries = _read_journal_entries()
    for index, entry in enumerate(entries):
        if entry.get("id") == entry_id:
            updated = {
                **entry,
                "date": request.date,
                "trades": [trade.dict() for trade in request.trades],
                "reflection": request.reflection,
                "tags": request.tags,
                "good": request.good,
                "bad": request.bad,
                "ugly": request.ugly,
                "goals": request.goals,
                "updatedAt": datetime.utcnow().isoformat(),
            }
            entries[index] = updated
            _write_journal_entries(entries)
            return {"success": True, "entry": updated}
    return {"error": "Journal entry not found"}


@app.delete("/api/journal/entries/{entry_id}")
def delete_journal_entry(entry_id: str):
    entries = _read_journal_entries()
    filtered = [entry for entry in entries if entry.get("id") != entry_id]
    if len(filtered) == len(entries):
        return {"error": "Journal entry not found"}
    _write_journal_entries(filtered)
    return {"success": True}


@app.post("/api/trade-chat")
def trade_chat(request: TradeChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    entries = _read_journal_entries()
    context = _recent_trade_context(entries)

    if not api_key:
        return {
            "reply": (
                "I can see your trade-journal endpoint is connected, but OPENAI_API_KEY is not set yet. "
                "Once that key is configured, I can coach you using recent trades. "
                f"Current context sample: {context[:500]}"
            )
        }

    system_prompt = (
        "You are a concise trading performance coach. "
        "Use the user's recent journal trades as your source of truth. "
        "Focus on risk management, execution quality, and psychology habits."
    )
    user_prompt = (
        f"Recent trade journal context:\n{context}\n\n"
        f"User question: {request.message}"
    )

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.4,
            },
            timeout=25,
        )
        if response.status_code != 200:
            return {"reply": "AI service is currently unavailable. Please try again shortly."}

        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        return {"reply": content}
    except Exception:
        return {"reply": "I hit an error while contacting ChatGPT. Please retry in a moment."}


@app.post("/api/broker/tradovate/connect")
def tradovate_connect(request: TradovateConnectRequest):
    base_url = _tradovate_base_url(request.isDemo)
    payload = {
        "name": request.name,
        "password": request.password,
        "appId": request.appId,
        "appVersion": request.appVersion,
        "cid": str(request.cid),
        "sec": request.sec,
    }
    try:
        response = requests.post(
            f"{base_url}/auth/accesstokenrequest",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=20,
        )
        data = response.json()
    except Exception as error:
        return {"error": f"Failed to connect to Tradovate: {str(error)}"}

    if response.status_code != 200 or not data.get("accessToken"):
        return {"error": data.get("errorText") or "Tradovate authentication failed."}

    access_token = data.get("accessToken")
    accounts_response = requests.get(
        f"{base_url}/account/list",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    accounts = accounts_response.json() if accounts_response.ok else []

    connection = {
        "isConnected": True,
        "isDemo": request.isDemo,
        "baseUrl": base_url,
        "username": request.name,
        "appId": request.appId,
        "cid": str(request.cid),
        "accessToken": access_token,
        "expirationTime": data.get("expirationTime"),
        "userId": data.get("userId"),
        "accounts": accounts if isinstance(accounts, list) else [],
        "connectedAt": datetime.utcnow().isoformat(),
    }
    _write_tradovate_connection(connection)
    return {
        "success": True,
        "message": "Tradovate connected successfully.",
        "status": {
            "isConnected": True,
            "isDemo": request.isDemo,
            "username": request.name,
            "accountCount": len(connection["accounts"]),
            "expirationTime": connection.get("expirationTime"),
        },
    }


@app.post("/api/journal/send-eod-email-now")
def send_eod_email_now():
    return _send_eod_email_now()


@app.post("/api/waitlist/send-live-announcement")
def send_live_announcement(request: LaunchAnnouncementRequest):
    waitlist_records = get_waitlist_emails()
    recipients: List[str] = []
    for record in waitlist_records:
        if isinstance(record, dict):
            email = record.get("email")
            status = record.get("status", "active")
            if email and status == "active" and "@" in email:
                recipients.append(email.strip())
        elif isinstance(record, str) and "@" in record:
            recipients.append(record.strip())

    recipients = sorted(list(set(recipients)))
    cta_url = request.ctaUrl or os.getenv("MIND2PROFIT_LOGIN_URL", "https://mind2profit.com")
    html = _build_launch_announcement_html(cta_url)
    result = _send_bulk_html_email(recipients, request.subject or "Mind2Profit is now LIVE - Opening Sale", html)
    if not result.get("success"):
        return {"success": False, "error": result.get("error"), "recipientsFound": len(recipients)}
    return {
        "success": True,
        "message": "Launch announcement sent.",
        "recipientsFound": len(recipients),
        "sentCount": result.get("sentCount", 0),
        "ctaUrl": cta_url,
    }


@app.get("/api/journal/eod-email-status")
def eod_email_status():
    state = _read_email_reminder_state()
    enabled = os.getenv("ENABLE_DAILY_JOURNAL_EMAILS", "false").lower() == "true"
    return {
        "enabled": enabled,
        "scheduleHour": int(os.getenv("DAILY_REMINDER_HOUR", "17")),
        "scheduleMinute": int(os.getenv("DAILY_REMINDER_MINUTE", "0")),
        "lastSentDate": state.get("last_sent_date"),
        "lastSentAt": state.get("last_sent_at"),
        "lastResult": state.get("last_result"),
    }


@app.post("/api/broker/tradovate/connect-token")
def tradovate_connect_token(request: TradovateTokenConnectRequest):
    base_url = _tradovate_base_url(request.isDemo)
    try:
        accounts_response = requests.get(
            f"{base_url}/account/list",
            headers={"Authorization": f"Bearer {request.accessToken}"},
            timeout=20,
        )
        if not accounts_response.ok:
            return {"error": "Token is invalid or expired for this environment."}
        accounts_payload = accounts_response.json()
        accounts = accounts_payload if isinstance(accounts_payload, list) else []
    except Exception as error:
        return {"error": f"Failed to validate Tradovate token: {str(error)}"}

    connection = {
        "isConnected": True,
        "isDemo": request.isDemo,
        "baseUrl": base_url,
        "username": request.username or "manual-token",
        "accessToken": request.accessToken,
        "accounts": accounts,
        "connectedAt": datetime.utcnow().isoformat(),
        "connectionMode": "token",
    }
    _write_tradovate_connection(connection)
    return {
        "success": True,
        "message": "Tradovate token connected.",
        "status": {
            "isConnected": True,
            "isDemo": request.isDemo,
            "username": connection["username"],
            "accountCount": len(accounts),
        },
    }


@app.post("/api/broker/tradovate/bypass")
def tradovate_bypass():
    connection = {
        "isConnected": True,
        "isDemo": True,
        "baseUrl": _tradovate_base_url(True),
        "username": "bypass-test-user",
        "accessToken": "bypass-token",
        "accounts": [
            {"id": 900001, "name": "SIM-TEST-001", "active": True},
            {"id": 900002, "name": "SIM-TEST-002", "active": True},
        ],
        "connectedAt": datetime.utcnow().isoformat(),
        "connectionMode": "bypass",
    }
    _write_tradovate_connection(connection)
    return {"success": True, "message": "Bypass mode enabled for testing."}


@app.get("/api/broker/tradovate/oauth-url")
def tradovate_oauth_url(isDemo: bool = True):
    base = _tradovate_oauth_base_url(isDemo)
    client_id = os.getenv("TRADOVATE_OAUTH_CLIENT_ID")
    redirect_uri = os.getenv("TRADOVATE_OAUTH_REDIRECT_URI")

    if client_id and redirect_uri:
        from urllib.parse import urlencode

        query = urlencode(
            {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": redirect_uri,
            }
        )
        return {"url": f"{base}?{query}", "isConfigured": True}

    return {"url": base, "isConfigured": False}


@app.get("/api/broker/tradovate/status")
def tradovate_status():
    connection = _read_tradovate_connection()
    if not connection:
        return {"isConnected": False}

    return {
        "isConnected": True,
        "isDemo": connection.get("isDemo", True),
        "username": connection.get("username"),
        "appId": connection.get("appId"),
        "accountCount": len(connection.get("accounts", [])),
        "accounts": connection.get("accounts", []),
        "expirationTime": connection.get("expirationTime"),
        "connectedAt": connection.get("connectedAt"),
        "connectionMode": connection.get("connectionMode", "credentials"),
    }


@app.post("/api/broker/tradovate/sync")
def tradovate_sync():
    connection = _read_tradovate_connection()
    if not connection or not connection.get("accessToken"):
        return {"error": "Tradovate is not connected."}

    try:
        accounts_response = requests.get(
            f"{connection['baseUrl']}/account/list",
            headers={"Authorization": f"Bearer {connection['accessToken']}"},
            timeout=20,
        )
        if not accounts_response.ok:
            return {"error": "Failed to refresh Tradovate accounts. Reconnect required."}
        accounts_payload = accounts_response.json()
        accounts = accounts_payload if isinstance(accounts_payload, list) else []
        connection["accounts"] = accounts
        connection["lastSyncAt"] = datetime.utcnow().isoformat()
        _write_tradovate_connection(connection)
        return {
            "success": True,
            "message": "Tradovate sync completed.",
            "accountCount": len(accounts),
            "lastSyncAt": connection["lastSyncAt"],
            "note": "Trade fill ingestion endpoint is the next step once account scope is confirmed.",
        }
    except Exception as error:
        return {"error": f"Sync failed: {str(error)}"}


@app.delete("/api/broker/tradovate/disconnect")
def tradovate_disconnect():
    _delete_tradovate_connection()
    return {"success": True, "message": "Tradovate disconnected."}


@app.on_event("startup")
def start_daily_email_scheduler():
    global _email_scheduler_thread
    enabled = os.getenv("ENABLE_DAILY_JOURNAL_EMAILS", "false").lower() == "true"
    if not enabled:
        return
    if _email_scheduler_thread and _email_scheduler_thread.is_alive():
        return
    _email_scheduler_thread = threading.Thread(target=_daily_email_scheduler_loop, daemon=True)
    _email_scheduler_thread.start()

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
