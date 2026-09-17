import yfinance as yf
from langfuse import observe


@observe(name="market-snapshot")
def market_snapshot(ticker: str, period: str = "3mo") -> dict:
    symbol = ticker.upper().strip()
    symbol = symbol if "." in symbol else symbol + ".NS"
    hist = yf.Ticker(symbol).history(period=period, interval="1d", auto_adjust=True)
    if hist.empty:
        return {"ticker": symbol, "period": period, "status": "unavailable"}

    close = hist["Close"].dropna()
    ret = (float(close.iloc[-1]) / float(close.iloc[0]) - 1) * 100 if len(close) > 1 else 0.0
    return {
        "ticker": symbol,
        "period": period,
        "start": str(close.index[0].date()),
        "end": str(close.index[-1].date()),
        "first_close": round(float(close.iloc[0]), 2),
        "last_close": round(float(close.iloc[-1]), 2),
        "return_percent": round(ret, 2),
        "source": "yfinance",
    }
