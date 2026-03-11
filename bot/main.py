# bot/main.py
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8584253560:AAEtuulfRCGtnZESvhW9hgwJb7GPkzBcqDs"
CHAT_ID = "5181567854"  # число

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Бот запущений і працює!")
    print(f"Повідомлення надіслано chat_id={update.message.chat_id}")

async def send_test_message(application):
    await application.bot.send_message(chat_id=CHAT_ID, text="Тестове повідомлення при запуску")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команда /start
    app.add_handler(CommandHandler("start", start))

    # Надсилання тестового повідомлення після старту
    app.post_init = send_test_message

    print("Бот запущений 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()