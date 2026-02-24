#!/usr/bin/env python3
"""Fetch price data for a ticker. Usage: python skills/price.py AAPL [period]"""
import json, sys
import yfinance as yf

ticker = sys.argv[1]
period = sys.argv[2] if len(sys.argv) > 2 else "6mo"

t = yf.Ticker(ticker)
df = t.history(period=period)

if df.empty:
    print(json.dumps({"error": f"No data for {ticker}"}))
    sys.exit(1)

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest
change = ((latest["Close"] - prev["Close"]) / prev["Close"]) * 100
avg_vol = float(df["Volume"].tail(30).mean())

out = {
    "ticker": ticker,
    "current": round(float(latest["Close"]), 2),
    "prev_close": round(float(prev["Close"]), 2),
    "change_pct": round(change, 2),
    "high": round(float(latest["High"]), 2),
    "low": round(float(latest["Low"]), 2),
    "volume": int(latest["Volume"]),
    "avg_volume_30d": int(avg_vol),
    "volume_ratio": round(int(latest["Volume"]) / avg_vol, 2) if avg_vol > 0 else 0,
    "period_high": round(float(df["Close"].max()), 2),
    "period_low": round(float(df["Close"].min()), 2),
}
print(json.dumps(out, indent=2))
