import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Get BTC price from MEXC
response = requests.get(
    "https://api.mexc.com/api/v3/ticker/price?symbol=BTCUSDT"
)

btc_price = response.json()["price"]

message = f"📈 BTCUSDT Price: ${btc_price}"

telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    telegram_url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
