#!/usr/bin/env python3
"""Fetch peer comparison data. Usage: python skills/peers.py AAPL"""
import json, sys
import yfinance as yf

ticker = sys.argv[1]
t = yf.Ticker(ticker)
info = t.info

sector = info.get("sector", "")
industry = info.get("industry", "")
industry_key = info.get("industryKey", "")

# Find peers
peer_tickers = []
try:
    if industry_key:
        ind = yf.Industry(industry_key)
        top = ind.top_companies
        if top is not None and not top.empty:
            peer_tickers = [str(s) for s in top.index.tolist() if str(s) != ticker.upper()][:5]
except Exception:
    pass

# Compare
comparison = []
for sym in [ticker] + peer_tickers:
    try:
        ti = yf.Ticker(sym)
        ii = ti.info
        comparison.append({
            "ticker": sym,
            "name": ii.get("shortName", sym),
            "market_cap": ii.get("marketCap"),
            "pe": round(float(ii["trailingPE"]), 2) if ii.get("trailingPE") else None,
            "margin_pct": round(float(ii["profitMargins"]) * 100, 2) if ii.get("profitMargins") else None,
            "growth_pct": round(float(ii["revenueGrowth"]) * 100, 2) if ii.get("revenueGrowth") else None,
            "beta": round(float(ii["beta"]), 2) if ii.get("beta") else None,
        })
    except Exception:
        comparison.append({"ticker": sym, "error": "fetch failed"})

out = {
    "ticker": ticker,
    "sector": sector,
    "industry": industry,
    "peers": peer_tickers,
    "comparison": comparison,
}
print(json.dumps(out, indent=2, default=str))
