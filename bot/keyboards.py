from telegram import ReplyKeyboardMarkup, KeyboardButton

# ---------------------------
# Головне меню (persistent)
# ---------------------------
def main_menu():
    keyboard = [
        [KeyboardButton("📊 Монети")],
        [KeyboardButton("➕ Додати пару")],
        [KeyboardButton("🤖 Авто сигнали")],
        [KeyboardButton("📜 Історія")],
        [KeyboardButton("⚙️ Налаштування")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)

# ---------------------------
# Кнопка назад
# ---------------------------
def back_button():
    keyboard = [[KeyboardButton("⬅️ Назад")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ---------------------------
# Меню таймфреймів
# ---------------------------
def timeframe_menu():
    keyboard = [
        [KeyboardButton("⏱ 1m"), KeyboardButton("⏱ 15m")],
        [KeyboardButton("⏱ 1h"), KeyboardButton("⏱ 1d")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ---------------------------
# Меню стратегій
# ---------------------------
def strategy_menu():
    keyboard = [
        [KeyboardButton("EMA Trend"), KeyboardButton("RSI")],
        [KeyboardButton("MACD"), KeyboardButton("Volume")],
        [KeyboardButton("VWAP"), KeyboardButton("Market Structure")],
        [KeyboardButton("Breakout"), KeyboardButton("Machine Learning")],
        [KeyboardButton("⬅️ Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ---------------------------
# Динамічне меню монет користувача
# ---------------------------
def coins_menu(user_pairs):
    """
    user_pairs: list[str] - список символів монет користувача
    """
    keyboard = [[KeyboardButton(symbol)] for symbol in user_pairs]
    keyboard.append([KeyboardButton("⬅️ Назад")])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)