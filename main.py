print("MAIN START")

from config import CORE_COINS
print("CONFIG LOADED")

from scanner import analyze_symbol
print("SCANNER LOADED")

from telegram_bot import send_signal
print("TELEGRAM LOADED")

from stats import cooldown_active
print("STATS LOADED")


def main():
    print("ENTERING MAIN")

    if cooldown_active():
        print("COOLDOWN ACTIVE")
        return

    for coin in CORE_COINS:
        print(f"SCANNING {coin}")

        try:
            signal = analyze_symbol(coin)

            print(f"ANALYSIS COMPLETE {coin}")

            if not signal["valid"]:
                print(
                    f"NO SIGNAL {coin} | "
                    f"Score={signal['score']} | "
                    f"RSI={signal['rsi']} | "
                    f"Price={signal['price']}"
                )
                continue

            send_signal(
                coin=signal["symbol"],
                direction=signal["direction"],
                current_price=signal["price"],
                entry_low=signal["price"],
                entry_high=signal["price"],
                expected_move=signal["expected_move"],
                stop_loss=0.4,
                score=signal["score"],
                reasons=signal["reasons"]
            )

            print(f"SIGNAL SENT {coin}")

        except Exception as e:
            print(f"ERROR {coin}: {e}")


if __name__ == "__main__":
    main()
