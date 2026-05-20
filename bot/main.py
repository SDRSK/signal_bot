from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from handlers import start, handle_message, auto_signals
import asyncio

TOKEN = "ВСТАВ_СВІЙ_ТОКЕН"


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    await app.initialize()
    await app.start()

    asyncio.create_task(auto_signals(app))

    print("Bot started")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())