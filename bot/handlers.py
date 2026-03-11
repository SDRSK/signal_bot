from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards import main_menu, back_button
from database.db import SessionLocal
from database.models import User, UserPair
from bybit.api import check_symbol

# Додаємо аналіз
from analysis.analysis_service import analyze

# Старт бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.message.from_user.id)
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=telegram_id).first()

    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()

    await update.message.reply_text(
        "🚀 Крипто бот сигналів\n\nВиберіть дію:",
        reply_markup=main_menu()
    )
    db.close()

# Обробка всіх повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    telegram_id = str(update.message.from_user.id)
    db = SessionLocal()
    user = db.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id)
        db.add(user)
        db.commit()

    # Додати пару
    if text == "➕ Додати пару":
        await update.message.reply_text(
            "Напишіть пару\n\nПриклад:\nBTCUSDT",
            reply_markup=back_button()
        )
        db.close()
        return

    # Якщо користувач написав символ монети
    symbol = text.upper()
    if len(symbol) > 3:
        if not check_symbol(symbol):
            await update.message.reply_text("❌ Такої пари немає на Bybit", reply_markup=back_button())
            db.close()
            return

        existing_pair = db.query(UserPair).filter_by(user_id=user.id, symbol=symbol).first()
        if existing_pair:
            await update.message.reply_text(f"❌ Пара {symbol} вже додана", reply_markup=back_button())
            db.close()
            return

        # Додаємо пару
        pair = UserPair(symbol=symbol, user_id=user.id)
        db.add(pair)
        db.commit()

        # --------------------------------------------
        # Аналіз сигналів для нової пари
        # --------------------------------------------
        # Тут поки тестові дані, пізніше можна підключити реальні через API Bybit
        symbol_data = {
            "prices": [67000, 67100, 67250, 67300, 67400, 67350, 67500],
            "volumes": [100, 120, 150, 130, 200, 180, 250]
        }

        signal = analyze(symbol_data)

        await update.message.reply_text(
            f"✅ Пара {symbol} додана\n\n🚨 Сигнал:\n{symbol} {signal['final_signal']}\n"
            f"EMA: {signal['details']['EMA']}\n"
            f"RSI: {signal['details']['RSI']}\n"
            f"Volume: {signal['details']['Volume']}",
            reply_markup=main_menu()
        )
        db.close()
        return

    # Меню монет
    if text == "📊 Монети":
        pairs = db.query(UserPair).filter_by(user_id=user.id).all()
        msg = "Ваші монети:\n" + "\n".join([p.symbol for p in pairs])
        await update.message.reply_text(msg if pairs else "Пари не додані", reply_markup=back_button())
        db.close()
        return

    # Авто сигнали
    if text == "🤖 Авто сигнали":
        await update.message.reply_text("Налаштування авто сигналів", reply_markup=back_button())
        db.close()
        return

    # Історія сигналів
    if text == "📜 Історія":
        await update.message.reply_text("Історія сигналів", reply_markup=back_button())
        db.close()
        return

    # Налаштування бота
    if text == "⚙️ Налаштування":
        await update.message.reply_text("Налаштування бота", reply_markup=back_button())
        db.close()
        return

    # Кнопка назад
    if text == "⬅️ Назад":
        await update.message.reply_text("Повернулися в головне меню", reply_markup=main_menu())
        db.close()
        return

    # Не зрозумів
    await update.message.reply_text("Не зрозумів 😅, оберіть дію з меню", reply_markup=main_menu())
    db.close()