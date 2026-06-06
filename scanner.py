import requests
import pandas as pd
from config import (
    MEXC_BASE_URL,
    RSI_PERIOD,
    EMA_FAST,
    EMA_MID,
    EMA_SLOW,
    VOLUME_LOOKBACK,
    VOLUME_SPIKE_MULTIPLIER,
    MIN_SCORE,
)


def get_klines(symbol, interval="15m", limit=250):
    url = (
        f"{MEXC_BASE_URL}/api/v3/klines"
        f"?symbol={symbol}&interval={interval}&limit={limit}"
    )

    response = requests.get(url, timeout=15)

    data = response.json()

    df = pd.DataFrame(data)

    df.columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "trades",
        "buy_base",
        "buy_quote",
        "ignore",
    ]

    numeric_cols = ["open", "high", "low", "close", "volume"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    return df


def calculate_rsi(series, period=14):
    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def analyze_symbol(symbol):
    df = get_klines(symbol)

    close = df["close"]

    df["ema20"] = close.ewm(span=EMA_FAST, adjust=False).mean()
    df["ema50"] = close.ewm(span=EMA_MID, adjust=False).mean()
    df["ema200"] = close.ewm(span=EMA_SLOW, adjust=False).mean()

    df["rsi"] = calculate_rsi(close, RSI_PERIOD)

    current_price = float(df["close"].iloc[-1])

    ema20 = float(df["ema20"].iloc[-1])
    ema50 = float(df["ema50"].iloc[-1])
    ema200 = float(df["ema200"].iloc[-1])

    rsi = float(df["rsi"].iloc[-1])

    current_volume = float(df["volume"].iloc[-1])

    avg_volume = (
        df["volume"]
        .tail(VOLUME_LOOKBACK)
        .mean()
    )

    score = 0

    reasons = []

    if ema20 > ema50 > ema200:
        score += 35
        reasons.append("EMA alignment")

    if 50 <= rsi <= 70:
        score += 20
        reasons.append("RSI strength")

    if current_volume > avg_volume * VOLUME_SPIKE_MULTIPLIER:
        score += 25
        reasons.append("Volume spike")

    if current_price > ema20:
        score += 20
        reasons.append("Price above EMA20")

    expected_move = round(
        abs(current_price - ema20)
        / current_price
        * 100
        + 0.4,
        2,
    )

    signal = {
        "symbol": symbol,
        "score": score,
        "price": round(current_price, 6),
        "expected_move": expected_move,
        "ema20": round(ema20, 6),
        "ema50": round(ema50, 6),
        "ema200": round(ema200, 6),
        "rsi": round(rsi, 2),
        "reasons": "\n".join(
            f"✓ {x}" for x in reasons
        ),
        "valid": score >= MIN_SCORE,
    }

    return signal
