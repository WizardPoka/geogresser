# ====================================================================================

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import load_dotenv, find_dotenv

from app.handlers.user_router import user_router
# from app.common.bot_cmds_list import private
# ====================================================================================

load_dotenv(find_dotenv())

async def main():
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()

    dp.include_router(user_router)

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")  

# ====================================================================================