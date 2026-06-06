import json
import os
from datetime import datetime, timedelta

DATA_FILE = "data.json"


def load_stats():
    if not os.path.exists(DATA_FILE):
        return {
            "wins": 0,
            "losses": 0,
            "breakeven": 0,
            "cooldown_until": None,
            "sent_signals": {}
        }

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_stats(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def record_win():
    data = load_stats()

    data["wins"] += 1

    now = datetime.utcnow()

    tomorrow = (
        now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        + timedelta(days=1)
    )

    data["cooldown_until"] = tomorrow.isoformat()

    save_stats(data)


def record_loss():
    data = load_stats()

    data["losses"] += 1

    save_stats(data)


def record_breakeven():
    data = load_stats()

    data["breakeven"] += 1

    save_stats(data)


def cooldown_active():
    data = load_stats()

    cooldown_until = data.get(
        "cooldown_until"
    )

    if not cooldown_until:
        return False

    cooldown_time = datetime.fromisoformat(
        cooldown_until
    )

    return datetime.utcnow() < cooldown_time


def signal_blocked(
    coin,
    direction,
    hours=1
):
    data = load_stats()

    key = f"{coin}_{direction}"

    sent_signals = data.get(
        "sent_signals",
        {}
    )

    if key not in sent_signals:
        return False

    signal_time = datetime.fromisoformat(
        sent_signals[key]
    )

    return (
        datetime.utcnow() - signal_time
    ) < timedelta(hours=hours)


def record_signal(
    coin,
    direction
):
    data = load_stats()

    key = f"{coin}_{direction}"

    data["sent_signals"][key] = (
        datetime.utcnow().isoformat()
    )

    save_stats(data)
