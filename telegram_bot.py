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
    reasons,
    confidence_colour="🟠"
):
    if direction == "LONG":
        tp_price = round(
            current_price * (1 + expected_move / 100),
            6
        )

        sl_price = round(
            current_price * (1 - stop_loss / 100),
            6
        )

    else:
        tp_price = round(
            current_price * (1 - expected_move / 100),
            6
        )

        sl_price = round(
            current_price * (1 + stop_loss / 100),
            6
        )

    risk = abs(current_price - sl_price)
    reward = abs(tp_price - current_price)

    if risk > 0:
        rr = round(reward / risk, 2)
    else:
        rr = 0

    message = f"""
🚨 {direction} SIGNAL

Coin: {coin}

Current Price:
{current_price}

Take Profit:
{tp_price}

Stop Loss:
{sl_price}

Expected Move:
{expected_move:.2f}%

Risk / Reward:
{rr}:1

{confidence_colour} Confidence:
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
