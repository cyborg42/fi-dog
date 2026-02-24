#!/usr/bin/env python3
"""Fetch options sentiment data. Usage: python skills/options.py AAPL"""
import json, sys
import yfinance as yf

ticker = sys.argv[1]
t = yf.Ticker(ticker)

try:
    exps = t.options
except Exception:
    print(json.dumps({"error": f"No options data for {ticker}"}))
    sys.exit(1)

if not exps:
    print(json.dumps({"error": "No expirations available"}))
    sys.exit(1)

total_call_oi = total_put_oi = 0
total_call_vol = total_put_vol = 0
iv_calls, iv_puts = [], []

for exp in exps[:3]:
    try:
        chain = t.option_chain(exp)
        total_call_oi += int(chain.calls["openInterest"].sum())
        total_put_oi += int(chain.puts["openInterest"].sum())
        total_call_vol += int(chain.calls["volume"].fillna(0).sum())
        total_put_vol += int(chain.puts["volume"].fillna(0).sum())
        iv_calls.extend(chain.calls["impliedVolatility"].dropna().tolist())
        iv_puts.extend(chain.puts["impliedVolatility"].dropna().tolist())
    except Exception:
        continue

out = {
    "ticker": ticker,
    "expirations_sampled": list(exps[:3]),
    "call_open_interest": total_call_oi,
    "put_open_interest": total_put_oi,
    "call_volume": total_call_vol,
    "put_volume": total_put_vol,
    "pcr_oi": round(total_put_oi / total_call_oi, 3) if total_call_oi else None,
    "pcr_volume": round(total_put_vol / total_call_vol, 3) if total_call_vol else None,
    "avg_iv_calls_pct": round(sum(iv_calls) / len(iv_calls) * 100, 2) if iv_calls else None,
    "avg_iv_puts_pct": round(sum(iv_puts) / len(iv_puts) * 100, 2) if iv_puts else None,
}
print(json.dumps(out, indent=2))
