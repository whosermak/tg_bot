from aiogram import Router, types
from aiogram.filters import Command
from services.nlp import parse_text
from services.db import execute, wait_db

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.reply("Дратути, задай мне вопрос по данным из бд и я на все отвечу!")



@router.message()
async def handle_message(message: types.Message):
    text = message.text

    sql = await parse_text(text)
    result = await execute(sql)

    await message.answer(str(result))