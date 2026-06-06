from config import CORE_COINS
from scanner import analyze_symbol
from telegram_bot import send_signal
from stats import cooldown_active


def main():
    if cooldown_active():
        print("Cooldown active")
        return

    for coin in CORE_COINS:
        try:
            signal = analyze_symbol(coin)

            if not signal["valid"]:
                continue

            send_signal(
                coin=signal["symbol"],
                direction="LONG",
                current_price=signal["price"],
                entry_low=signal["price"],
                entry_high=signal["price"],
                expected_move=signal["expected_move"],
                stop_loss=0.4,
                score=signal["score"],
                reasons=signal["reasons"]
            )

            print(f"Signal sent for {coin}")

        except Exception as e:
            print(f"Error on {coin}: {e}")


if __name__ == "__main__":
    main()
