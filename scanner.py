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

    df = df.iloc[:, :6]

    df.columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    for col in ["open", "high", "low", "close", "volume"]:
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


def get_trend(symbol):
    df = get_klines(symbol)

    close = df["close"]

    ema20 = close.ewm(
        span=EMA_FAST,
        adjust=False
    ).mean().iloc[-1]

    ema50 = close.ewm(
        span=EMA_MID,
        adjust=False
    ).mean().iloc[-1]

    ema200 = close.ewm(
        span=EMA_SLOW,
        adjust=False
    ).mean().iloc[-1]

    if ema20 > ema50 > ema200:
        return "BULLISH"

    if ema20 < ema50 < ema200:
        return "BEARISH"

    return "NEUTRAL"


def analyze_symbol(symbol):
    df = get_klines(symbol)

    close = df["close"]

    df["ema20"] = close.ewm(
        span=EMA_FAST,
        adjust=False
    ).mean()

    df["ema50"] = close.ewm(
        span=EMA_MID,
        adjust=False
    ).mean()

    df["ema200"] = close.ewm(
        span=EMA_SLOW,
        adjust=False
    ).mean()

    df["rsi"] = calculate_rsi(
        close,
        RSI_PERIOD
    )

    current_price = float(df["close"].iloc[-1])

    ema20 = float(df["ema20"].iloc[-1])
    ema50 = float(df["ema50"].iloc[-1])
    ema200 = float(df["ema200"].iloc[-1])

    rsi = float(df["rsi"].iloc[-1])

    current_volume = float(
        df["volume"].iloc[-1]
    )

    avg_volume = (
        df["volume"]
        .tail(VOLUME_LOOKBACK)
        .mean()
    )

    btc_trend = get_trend("BTCUSDT")

    long_score = 0
    short_score = 0

    long_reasons = []
    short_reasons = []

    # LONG

    if ema20 > ema50 > ema200:
        long_score += 35
        long_reasons.append(
            "EMA bullish alignment"
        )

    if current_price > ema20:
        long_score += 15
        long_reasons.append(
            "Price above EMA20"
        )

    if 55 <= rsi <= 70:
        long_score += 10
        long_reasons.append(
            "RSI bullish"
        )

    if (
        current_volume >
        avg_volume *
        VOLUME_SPIKE_MULTIPLIER
    ):
        long_score += 15
        long_reasons.append(
            "Volume expansion"
        )

    if btc_trend == "BULLISH":
        long_score += 25
        long_reasons.append(
            "BTC bullish"
        )

    # SHORT

    if ema20 < ema50 < ema200:
        short_score += 35
        short_reasons.append(
            "EMA bearish alignment"
        )

    if current_price < ema20:
        short_score += 15
        short_reasons.append(
            "Price below EMA20"
        )

    if 30 <= rsi <= 45:
        short_score += 10
        short_reasons.append(
            "RSI bearish"
        )

    if (
        current_volume >
        avg_volume *
        VOLUME_SPIKE_MULTIPLIER
    ):
        short_score += 15
        short_reasons.append(
            "Volume expansion"
        )

    if btc_trend == "BEARISH":
        short_score += 25
        short_reasons.append(
            "BTC bearish"
        )

    if long_score >= short_score:
        direction = "LONG"
        score = long_score
        reasons = "\n".join(
            f"✓ {x}" for x in long_reasons
        )
    else:
        direction = "SHORT"
        score = short_score
        reasons = "\n".join(
            f"✓ {x}" for x in short_reasons
        )

    if score >= 85:
        confidence_colour = "🟢"
    elif score >= 70:
        confidence_colour = "🟠"
    else:
        confidence_colour = "🔴"

    expected_move = round(
        (
            abs(current_price - ema20)
            / current_price
            * 100
        ) + 0.5,
        2,
    )

    signal = {
        "symbol": symbol,
        "direction": direction,
        "score": score,
        "confidence_colour": confidence_colour,
        "price": round(current_price, 6),
        "expected_move": expected_move,
        "ema20": round(ema20, 6),
        "ema50": round(ema50, 6),
        "ema200": round(ema200, 6),
        "rsi": round(rsi, 2),
        "reasons": reasons,
        "valid": score >= MIN_SCORE,
    }

    return signal
