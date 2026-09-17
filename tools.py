"""Three small tools: web search, market OHLCV, and percentage growth."""

import asyncio
from math import isfinite
from agno.tools import tool
import yfinance as yf
from agno.tools.tavily import TavilyTools


def _yahoo_symbol(ticker: str, exchange: str) -> str:
    symbol = ticker.strip().upper()
    exchange = exchange.strip().upper()
    if not symbol:
        raise ValueError("ticker cannot be empty")
    if exchange not in {"AUTO", "NSE", "BSE", "US"}:
        raise ValueError("exchange must be AUTO, NSE, BSE, or US")
    if "." in symbol or exchange in {"AUTO", "US"}:
        return symbol
    return f"{symbol}.NS" if exchange == "NSE" else f"{symbol}.BO"


def _number(value, *, integer: bool = False):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if not isfinite(value):
        return None
    return int(value) if integer else round(value, 4)




@tool(
    description="Retrieve daily OHLCV market data from Yahoo Finance.",
    instructions="""
    Use this tool for daily historical stock-price questions, including
    opening price, intraday high/low, closing price, and trading volume.

    - Use the ticker supplied by the user.
    - Use exchange="AUTO" unless the user explicitly specifies an exchange.
    - Use period="1mo" by default.
    - Use "1d" only when the user asks for the latest trading day.
    - Use "5d" for the latest five trading days.
    - Use max_rows to limit the returned daily records, up to 60.
    - Treat latest_market_day as the latest available trading day; it may
      precede the current calendar day on weekends and market holidays.
    - Report the returned values only; do not infer unavailable market data.
    """,
)
async def market_ohlcv(
    ticker: str,
    period: str = "1mo",
    exchange: str = "AUTO",
    max_rows: int = 30,
) -> dict:
    """Return daily Open, High, Low, Close and Volume from Yahoo Finance."""
    symbol = _yahoo_symbol(ticker, exchange)
    aliases = {"1m": "1mo", "3m": "3mo", "6m": "6mo"}
    period = aliases.get(period.strip().lower(), period.strip().lower())
    allowed = {"1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "ytd", "max"}

    if period not in allowed:
        raise ValueError("Unsupported period")
    if not 1 <= max_rows <= 60:
        raise ValueError("max_rows must be between 1 and 60")

    fetch_period = {"1d": "5d", "5d": "1mo"}.get(period, period)
    row_limit = {"1d": 1, "5d": 5}.get(period, max_rows)

    try:
        history = await asyncio.to_thread(
            yf.Ticker(symbol).history,
            period=fetch_period,
            interval="1d",
            auto_adjust=False,
        )
    except Exception as error:
        return {"symbol": symbol, "error": f"Could not fetch market data: {error}"}

    if history is None or history.empty:
        return {"symbol": symbol, "error": "No market data was returned"}

    rows = []
    for date, values in history.tail(row_limit).iterrows():
        rows.append(
            {
                "date": date.date().isoformat(),
                "open": _number(values.get("Open")),
                "high": _number(values.get("High")),
                "low": _number(values.get("Low")),
                "close": _number(values.get("Close")),
                "volume": _number(values.get("Volume"), integer=True),
            }
        )

    return {
        "symbol": symbol,
        "latest_market_day": rows[-1]["date"],
        "rows": rows,
        "note": "On a weekend or holiday, latest_market_day is the previous trading day.",
    }

def create_tools() -> list:
    """Return the tools in the same order used during the workshop."""
    web_search = TavilyTools()
    return [web_search, market_ohlcv]
