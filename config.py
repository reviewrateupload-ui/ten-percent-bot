# Coins that are always scanned

CORE_COINS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "SUIUSDT",
    "DOGEUSDT",
    "LINKUSDT",
    "AVAXUSDT",
    "ADAUSDT",
    "PEPEUSDT",
    "HYPEUSDT"
]

# Dynamic high-volume pairs
DYNAMIC_PAIRS = 5

# Scanner settings
SCAN_INTERVAL = 300  # 5 minutes

# Signal settings
MIN_SCORE = 60
HIGH_CONFIDENCE_SCORE = 85

# Trade settings
MIN_EXPECTED_MOVE = 0.4

# Indicators
RSI_PERIOD = 14

EMA_FAST = 20
EMA_MID = 50
EMA_SLOW = 200

# Volume
VOLUME_LOOKBACK = 20
VOLUME_SPIKE_MULTIPLIER = 1.5

# BTC Filter
BTC_FILTER = True

# Cooldown
WIN_COOLDOWN_HOURS = 24

# Timeframes
TREND_TIMEFRAME = "1h"
CONFIRM_TIMEFRAME = "15m"
ENTRY_TIMEFRAME = "5m"

# MEXC
MEXC_BASE_URL = "https://api.mexc.com"
