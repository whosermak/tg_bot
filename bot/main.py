import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from handlers.messages import router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())