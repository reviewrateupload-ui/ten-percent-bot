import os
import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    return response.json()


def send_signal(
    coin,
    direction,
    current_price,
    entry_low,
    entry_high,
    expected_move,
    stop_loss,
    score,
    reasons
):
    message = f"""
🚨 LIVE SIGNAL

Coin: {coin}

Direction: {direction}

Current Price:
{current_price}

Entry Zone:
{entry_low} - {entry_high}

Expected Move:
{expected_move:.2f}%

Stop Loss:
{stop_loss:.2f}%

Confidence:
{score}/100

Reasons:
{reasons}
"""

    return send_message(message)


def send_stats(stats):
    message = f"""
📊 BOT STATS

Wins: {stats['wins']}
Losses: {stats['losses']}
Breakeven: {stats['breakeven']}
"""

    return send_message(message)
