import asyncio
import requests
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

TOKEN = "8584253560:AAF0aaYmdP5pPe2bu-wPJF9KzhzCbAm2uNs"
CHAT_ID = "5181567854"

TOKENS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
TIMEFRAMES = {
    "15m ⏱️": "15",
    "1H ⏱️": "60"
}

signal_history = []

# ===== Отримання свічок Bybit v5 =====
def get_kline_data(symbol, interval):
    try:
        url = "https://api.bybit.com/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "limit": 200
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data["retCode"] != 0:
            print("API error:", data)
            return None

        klines = data["result"]["list"]
        closes = [float(k[4]) for k in klines]
        return closes[::-1]  # правильний порядок

    except Exception as e:
        print("Request error:", e)
        return None


# ===== EMA розрахунок =====
def calculate_ema(prices, period):
    if len(prices) < period:
        return None

    k = 2 / (period + 1)
    ema = prices[0]

    for price in prices[1:]:
        ema = price * k + ema * (1 - k)

    return round(ema, 2)


# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(t, callback_data=f"token_{t}")] for t in TOKENS]
    keyboard.append([InlineKeyboardButton("Історія сигналів 📜", callback_data="history")])

    await update.message.reply_text(
        "🚀 Виберіть токен:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ===== Кнопки =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "history":
        text = "📜 Історія сигналів:\n\n" + "\n\n".join(signal_history[-5:]) if signal_history else "Порожньо 📭"
        keyboard = [[InlineKeyboardButton("Назад 🔙", callback_data="back")]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))
        return

    if data == "back":
        await start(update, context)
        return

    if data.startswith("token_"):
        token = data.split("_")[1]
        keyboard = [[InlineKeyboardButton(tf, callback_data=f"tf_{token}_{TIMEFRAMES[tf]}")] for tf in TIMEFRAMES]
        keyboard.append([InlineKeyboardButton("Назад 🔙", callback_data="back")])

        await query.edit_message_text(
            f"📊 {token} — виберіть таймфрейм:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    if data.startswith("tf_"):
        _, token, interval = data.split("_")

        closes = get_kline_data(token, interval)

        if not closes:
            await query.edit_message_text("❌ Помилка отримання даних")
            return

        price = closes[-1]
        ema50 = calculate_ema(closes, 50)
        ema200 = calculate_ema(closes, 200)

        if not ema50 or not ema200:
            await query.edit_message_text("❌ Недостатньо даних")
            return

        signal = "LONG 📈" if ema50 > ema200 else "SHORT 📉"

        text = (
            f"💰 {token} | TF {interval}m\n\n"
            f"Ціна: {price}$\n"
            f"EMA50: {ema50}\n"
            f"EMA200: {ema200}\n\n"
            f"Сигнал: {signal}\n"
            f"⏰ {datetime.now().strftime('%H:%M:%S')}"
        )

        signal_history.append(text)

        keyboard = [[InlineKeyboardButton("Назад 🔙", callback_data=f"token_{token}")]]
        await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))


# ===== Авто сигнали =====
async def signal_loop(bot):
    while True:
        for token in TOKENS:
            closes = get_kline_data(token, "15")

            if closes:
                price = closes[-1]
                ema50 = calculate_ema(closes, 50)
                ema200 = calculate_ema(closes, 200)

                if ema50 and ema200:
                    signal = "LONG 📈" if ema50 > ema200 else "SHORT 📉"

                    text = (
                        f"🔥 Авто сигнал {token}\n"
                        f"Ціна: {price}$\n"
                        f"EMA50: {ema50} | EMA200: {ema200}\n"
                        f"{signal}\n"
                        f"{datetime.now().strftime('%H:%M:%S')}"
                    )

                    signal_history.append(text)
                    await bot.send_message(chat_id=CHAT_ID, text=text)

        await asyncio.sleep(300)


# ===== Запуск =====
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    async def post_init(application):
        application.create_task(signal_loop(application.bot))

    app.post_init = post_init
    app.run_polling()