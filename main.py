import time

from config import CORE_COINS

from scanner import analyze_symbol

from telegram_bot import send_signal

from stats import (
    cooldown_active,
    signal_blocked,
    record_signal,
)


def scan_market():
    print("STARTING SCAN")

    if cooldown_active():
        print("COOLDOWN ACTIVE")
        return

    for coin in CORE_COINS:
        try:
            print(f"SCANNING {coin}")

            signal = analyze_symbol(coin)

            if not signal["valid"]:
                print(
                    f"NO SIGNAL {coin} "
                    f"Score={signal['score']}"
                )
                continue

            if signal_blocked(
                signal["symbol"],
                signal["direction"],
                hours=1
            ):
                print(
                    f"BLOCKED "
                    f"{signal['symbol']} "
                    f"{signal['direction']}"
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
                reasons=signal["reasons"],
                confidence_colour=signal["confidence_colour"],
            )

            record_signal(
                signal["symbol"],
                signal["direction"]
            )

            print(
                f"SENT "
                f"{signal['symbol']} "
                f"{signal['direction']}"
            )

        except Exception as e:
            print(
                f"ERROR {coin}: {e}"
            )


def main():
    while True:
        scan_market()

        print(
            "WAITING 5 MINUTES"
        )

        time.sleep(300)


if __name__ == "__main__":
    main()
