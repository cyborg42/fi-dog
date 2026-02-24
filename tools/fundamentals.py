#!/usr/bin/env python3
"""Fetch fundamental data. Usage: python skills/fundamentals.py AAPL"""
import json, sys
import yfinance as yf

ticker = sys.argv[1]
t = yf.Ticker(ticker)
info = t.info

if not info:
    print(json.dumps({"error": f"No data for {ticker}"}))
    sys.exit(1)

def pct(key):
    v = info.get(key)
    return round(float(v) * 100, 2) if v else None

def num(key):
    v = info.get(key)
    return round(float(v), 2) if v else None

out = {
    "ticker": ticker,
    "name": info.get("shortName", ticker),
    "sector": info.get("sector"),
    "industry": info.get("industry"),
    "market_cap": info.get("marketCap"),
    "pe_trailing": num("trailingPE"),
    "pe_forward": num("forwardPE"),
    "eps_trailing": num("trailingEps"),
    "eps_forward": num("forwardEps"),
    "revenue": info.get("totalRevenue"),
    "revenue_growth_pct": pct("revenueGrowth"),
    "gross_margin_pct": pct("grossMargins"),
    "operating_margin_pct": pct("operatingMargins"),
    "profit_margin_pct": pct("profitMargins"),
    "free_cash_flow": info.get("freeCashflow"),
    "roe_pct": pct("returnOnEquity"),
    "debt_to_equity": num("debtToEquity"),
    "beta": num("beta"),
    "dividend_yield_pct": pct("dividendYield"),
    "52w_high": num("fiftyTwoWeekHigh"),
    "52w_low": num("fiftyTwoWeekLow"),
}

# Income statement summary
inc = t.financials
if inc is not None and not inc.empty:
    latest = inc.iloc[:, 0]
    out["annual_revenue"] = latest.get("Total Revenue")
    out["annual_operating_income"] = latest.get("Operating Income")
    out["annual_net_income"] = latest.get("Net Income")

print(json.dumps(out, indent=2, default=str))
