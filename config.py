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

# Number of extra high-volume coins
DYNAMIC_PAIRS = 5

# Scanner settings
SCAN_INTERVAL = 60

# Signal settings
MIN_SCORE = 85
MIN_EXPECTED_MOVE = 0.4

# Indicators
RSI_PERIOD = 14

EMA_FAST = 20
EMA_MID = 50
EMA_SLOW = 200

# Volume
VOLUME_LOOKBACK = 20
VOLUME_SPIKE_MULTIPLIER = 1.5

# Cooldown after a win
WIN_COOLDOWN_HOURS = 6

# Timeframes
TREND_TIMEFRAME = "1h"
CONFIRM_TIMEFRAME = "15m"
ENTRY_TIMEFRAME = "5m"

# MEXC
MEXC_BASE_URL = "https://api.mexc.com"
