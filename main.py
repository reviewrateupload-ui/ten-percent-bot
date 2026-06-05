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
ema50 = df[4].ewm(span=50).mean().iloc[-1]

current_price = df[4].iloc[-1]
if ema20 > ema50:
    trend = f"🟢 BTC Bullish\nEMA20: {ema20:.2f}\nEMA50: {ema50:.2f}"
else:
    trend = f"🔴 BTC Bearish\nEMA20: {ema20:.2f}\nEMA50: {ema50:.2f}"


telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": trend
    }
)

print(trend)
