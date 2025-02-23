import asyncio
import os
from datetime import datetime, timedelta

import dotenv
import random
import time

from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from trainings_app.tg_bot.temp_storage import tg_auth_data

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_ID = os.getenv('BOT_ID')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def generate_code():
    return str(random.randint(100000, 999999))


@dp.message_handler(commands=['start'])
async def start(message: Message):
    user_id = message.from_user.id
    code = generate_code()
    code_expiry = datetime.now() + timedelta(minutes=5)

    tg_auth_data[user_id] = {
        'code': code,
        'code_expiry': code_expiry,
    }

    await message.answer(
        f"""Enter the code to authorize: {code}. 
        The code will be active for 5 minutes."""
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
