from aiogram import Router, types
from aiogram.filters import Command
from services.nlp import parse_text
from services.db import execute

router = Router()


@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.reply("Стартовое сообщение")



@router.message()
async def handle_message(message: types.Message):
    text = message.text

    sql = await parse_text(text)
    result = await execute(sql)

    await message.answer(str(result) + " ... " + sql)