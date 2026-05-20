from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = [
        [KeyboardButton("📊 Монети")],
        [KeyboardButton("➕ Додати пару")],
        [KeyboardButton("🤖 Авто сигнали")],
        [KeyboardButton("📜 Історія")],
        [KeyboardButton("⏱ Таймфрейм")],
        [KeyboardButton("🧠 Стратегії")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def back_button():
    keyboard = [[KeyboardButton("⬅️ Назад")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def timeframe_menu():
    keyboard = [
        [KeyboardButton("⏱ 1m"), KeyboardButton("⏱ 5m")],
        [KeyboardButton("⏱ 10m"), KeyboardButton("⏱ 15m")],
        [KeyboardButton("⏱ 30m"), KeyboardButton("⏱ 1h")],
        [KeyboardButton("⏱ 2h"), KeyboardButton("⏱ 4h")],
        [KeyboardButton("⏱ 1d"), KeyboardButton("⏱ 1w")],
        [KeyboardButton("⏱ 1M")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def strategy_menu(selected=None):
    if selected is None:
        selected = []

    def mark(name):
        return f"✅ {name}" if name in selected else name

    keyboard = [
        [KeyboardButton(mark("EMA Trend")), KeyboardButton(mark("RSI"))],
        [KeyboardButton(mark("MACD")), KeyboardButton(mark("Volume"))],
        [KeyboardButton(mark("VWAP")), KeyboardButton(mark("Market Structure"))],
        [KeyboardButton(mark("Breakout")), KeyboardButton(mark("Machine Learning"))],
        [KeyboardButton("✔️ Готово")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def coins_menu(user_pairs):
    keyboard = [[KeyboardButton(symbol)] for symbol in user_pairs]
    keyboard.append([KeyboardButton("⬅️ Назад")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)