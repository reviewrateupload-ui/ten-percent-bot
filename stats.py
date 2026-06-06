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
            "cooldown_until": None
        }

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_stats(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def record_win():
    data = load_stats()

    data["wins"] += 1

    cooldown = datetime.utcnow() + timedelta(hours=6)

    data["cooldown_until"] = cooldown.isoformat()

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

    cooldown_until = data.get("cooldown_until")

    if not cooldown_until:
        return False

    cooldown_time = datetime.fromisoformat(cooldown_until)

    return datetime.utcnow() < cooldown_time
