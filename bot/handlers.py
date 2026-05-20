from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import *
from analysis_service import run_analysis
import asyncio

user_data_store = {}

DEFAULT_PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

STRATEGIES = ["EMA Trend", "RSI", "Volume"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_data_store[user_id] = {
        "pairs": DEFAULT_PAIRS.copy(),
        "timeframe": "1h",
        "strategies": [],
        "autosignal": False,
        "interval_sec": 60
    }

    await update.message.reply_text("🚀 Bot", reply_markup=main_menu())


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    user = user_data_store[user_id]

    if text == "⬅️ Назад":
        await update.message.reply_text("Меню", reply_markup=main_menu())

    elif text == "📊 Монети":
        await update.message.reply_text("Монети:", reply_markup=coins_menu(user["pairs"]))

    elif text == "⏱ Таймфрейм":
        await update.message.reply_text("Вибери TF", reply_markup=timeframe_menu())

    elif "⏱" in text:
        tf = text.replace("⏱ ", "")
        user["timeframe"] = tf
        await update.message.reply_text(f"TF: {tf}", reply_markup=main_menu())

    elif text == "🧠 Стратегії":
        await update.message.reply_text("Стратегії", reply_markup=strategy_menu(user["strategies"]))

    elif text.replace("✅ ", "") in STRATEGIES:
        s = text.replace("✅ ", "")

        if s in user["strategies"]:
            user["strategies"].remove(s)
        else:
            user["strategies"].append(s)

        await update.message.reply_text("ОК", reply_markup=strategy_menu(user["strategies"]))

    elif text == "✔️ Готово":
        await update.message.reply_text("Збережено", reply_markup=main_menu())

    elif text == "🤖 Авто сигнали":
        user["autosignal"] = not user["autosignal"]
        await update.message.reply_text(f"Авто: {user['autosignal']}", reply_markup=main_menu())

    elif text in user["pairs"]:
        msg = run_analysis(
            text,
            user["timeframe"],
            user["strategies"]
        )

        await update.message.reply_text(msg, reply_markup=main_menu())


async def auto_signals(app):
    while True:
        for user_id, user in user_data_store.items():
            if not user["autosignal"]:
                continue

            for pair in user["pairs"]:
                msg = run_analysis(
                    pair,
                    user["timeframe"],
                    user["strategies"]
                )

                await app.bot.send_message(user_id, msg)

        await asyncio.sleep(60)