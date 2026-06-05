import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

coins = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "SUIUSDT"
]

message = "📊 Live Prices\n\n"

for coin in coins:
    response = requests.get(
        f"https://api.mexc.com/api/v3/ticker/price?symbol={coin}"
    )

    price = response.json()["price"]

    message += f"{coin}: {price}\n"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
