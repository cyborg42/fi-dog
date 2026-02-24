#!/usr/bin/env python3
"""Fetch technical indicators. Usage: python skills/technicals.py AAPL"""
import json, sys
import yfinance as yf
import pandas_ta as ta

ticker = sys.argv[1]
t = yf.Ticker(ticker)
df = t.history(period="1y")

if df.empty:
    print(json.dumps({"error": f"No data for {ticker}"}))
    sys.exit(1)

close = df["Close"]

def safe(series):
    if series is None or series.empty:
        return None
    v = series.iloc[-1]
    return round(float(v), 2) if v == v else None  # NaN check

rsi = ta.rsi(close, length=14)
sma20 = ta.sma(close, length=20)
sma50 = ta.sma(close, length=50)
sma200 = ta.sma(close, length=200)
ema12 = ta.ema(close, length=12)
macd_df = ta.macd(close)
bbands = ta.bbands(close, length=20, std=2)

out = {
    "ticker": ticker,
    "RSI_14": safe(rsi),
    "SMA_20": safe(sma20),
    "SMA_50": safe(sma50),
    "SMA_200": safe(sma200),
    "EMA_12": safe(ema12),
}

if macd_df is not None and not macd_df.empty:
    out["MACD"] = round(float(macd_df.iloc[-1, 0]), 4)
    out["MACD_signal"] = round(float(macd_df.iloc[-1, 1]), 4)
    out["MACD_hist"] = round(float(macd_df.iloc[-1, 2]), 4)

if bbands is not None and not bbands.empty:
    out["BB_lower"] = round(float(bbands.iloc[-1, 0]), 2)
    out["BB_mid"] = round(float(bbands.iloc[-1, 1]), 2)
    out["BB_upper"] = round(float(bbands.iloc[-1, 2]), 2)

# Price vs MAs
cur = float(close.iloc[-1])
if out["SMA_50"]:
    out["price_vs_SMA50_pct"] = round((cur - out["SMA_50"]) / out["SMA_50"] * 100, 2)
if out["SMA_200"]:
    out["price_vs_SMA200_pct"] = round((cur - out["SMA_200"]) / out["SMA_200"] * 100, 2)

print(json.dumps(out, indent=2))
