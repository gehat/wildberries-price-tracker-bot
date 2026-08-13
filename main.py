from aiogram import executor
import loginning
from create_bot import dp
from handlers import client, other
import asyncio
from pay_and_scrapping import payments

client.register_handlers_client(dp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(other.PSql().search())
    loop.create_task(loginning.Reload_cooks().send_code())
    executor.start_polling(dp, skip_updates=False)