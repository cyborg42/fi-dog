#!/usr/bin/env python3
"""Fetch news for a ticker. Usage: python skills/news.py AAPL [days]"""
import json, sys, os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

ticker = sys.argv[1]
days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
articles = []

# Try finnhub first if API key is set
finnhub_key = os.environ.get("FINNHUB_API_KEY", "")
if finnhub_key:
    try:
        import finnhub
        client = finnhub.Client(api_key=finnhub_key)
        end = datetime.now()
        start = end - timedelta(days=days)
        raw = client.company_news(ticker, _from=start.strftime("%Y-%m-%d"), to=end.strftime("%Y-%m-%d"))
        for item in raw[:15]:
            articles.append({
                "headline": item.get("headline", ""),
                "source": item.get("source", ""),
                "url": item.get("url", ""),
                "datetime": datetime.fromtimestamp(item["datetime"]).isoformat() if item.get("datetime") else "",
            })
    except Exception:
        pass

# Fallback to Google News RSS
if not articles:
    try:
        import feedparser
        url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
        feed = feedparser.parse(url)
        for entry in feed.entries[:15]:
            articles.append({
                "headline": entry.get("title", ""),
                "source": entry.get("source", {}).get("title", "") if isinstance(entry.get("source"), dict) else "",
                "url": entry.get("link", ""),
                "datetime": entry.get("published", ""),
            })
    except Exception:
        pass

# Also try finnhub sentiment
sentiment = None
if finnhub_key:
    try:
        import finnhub
        client = finnhub.Client(api_key=finnhub_key)
        data = client.news_sentiment(ticker)
        if data and "sentiment" in data:
            s = data["sentiment"]
            sentiment = {
                "bullish_pct": round(s.get("bullishPercent", 0) * 100, 1),
                "bearish_pct": round(s.get("bearishPercent", 0) * 100, 1),
                "news_score": round(data.get("companyNewsScore", 0), 3),
            }
    except Exception:
        pass

print(json.dumps({"ticker": ticker, "articles": articles, "sentiment": sentiment}, indent=2))
