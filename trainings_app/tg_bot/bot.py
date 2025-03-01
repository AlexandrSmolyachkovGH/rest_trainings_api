import asyncio
import json
import os
from datetime import datetime, timedelta

import dotenv
import random
import time

from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message
from aiogram.filters import Command

from trainings_app.auth.utils.jwt_utils import decode_jwt
from trainings_app.db_redis.settings import redis_client

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_ID = os.getenv('BOT_ID')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)


def generate_code():
    return str(random.randint(100000, 999999))


@router.message(Command("start"))
async def start(message: Message):

    short_id = message.text.split(maxsplit=1)
    short_id = short_id[1] if len(short_id) > 1 else None
    if not short_id:
        await message.reply(f"To receive a verification code use a relevant link with an unique ID.")
    else:
        auth_token = await redis_client.get(short_id)
        user_data = decode_jwt(auth_token)
        if user_data.get("verified") is not False:
            await message.reply(f"Invalid token in the link.")
        else:
            code = generate_code()
            await redis_client.set(code, auth_token, ex=300)
            await message.answer(
                f"Hello {user_data['username']}!\n"
                f"Enter the code to authorize: {code}.\n"
                "The code will be active for 5 minutes."
            )


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_bot())
