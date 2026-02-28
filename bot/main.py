import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers.messages import router
from services.db import wait_db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)

async def main():
    await wait_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())