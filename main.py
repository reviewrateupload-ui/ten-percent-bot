import os
import requests
import pandas as pd

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://api.mexc.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=50"

response = requests.get(url)

candles = response.json()

df = pd.DataFrame(candles)

df[4] = df[4].astype(float)

ema20 = df[4].ewm(span=20).mean().iloc[-1]

current_price = df[4].iloc[-1]

if current_price > ema20:
    trend = "🟢 BTC Trend: Bullish"
else:
    trend = "🔴 BTC Trend: Bearish"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": trend
    }
)

print(trend)
