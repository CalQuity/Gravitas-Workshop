from __future__ import annotations

import asyncio
from datetime import datetime

import tools


class FakeFrame:
    def __init__(self, rows=None):
        self.rows = rows or []

    @property
    def empty(self):
        return not self.rows

    def tail(self, count):
        return FakeFrame(self.rows[-count:])

    def iterrows(self):
        return iter(self.rows)


def test_create_tools_lists_web_market_and_growth() -> None:
    registered = tools.create_tools()

    assert registered[0].name == "websearch"
    assert set(registered[0].functions) == {"web_search", "search_news"}
    assert registered[1].__name__ == "market_ohlcv"
    assert registered[2].__name__ == "calculate_growth"


def test_market_ohlcv_returns_the_latest_trading_day(monkeypatch) -> None:
    frame = FakeFrame(
        [
            (datetime(2026, 9, 11), {"Open": 100, "High": 105, "Low": 99, "Close": 104, "Volume": 1000}),
            (datetime(2026, 9, 14), {"Open": 104, "High": 108, "Low": 103, "Close": 107, "Volume": 1500}),
        ]
    )
    calls = []

    class FakeTicker:
        def __init__(self, symbol):
            assert symbol == "TCS.NS"

        def history(self, **kwargs):
            calls.append(kwargs)
            return frame

    monkeypatch.setattr(tools.yf, "Ticker", FakeTicker)

    result = asyncio.run(tools.market_ohlcv("TCS", period="1d", exchange="NSE"))

    assert calls == [{"period": "5d", "interval": "1d", "auto_adjust": False}]
    assert result["latest_market_day"] == "2026-09-14"
    assert result["rows"][0]["close"] == 107.0


def test_calculate_growth() -> None:
    assert tools.calculate_growth(100, 112)["growth_percent"] == 12.0

