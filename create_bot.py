import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import QiwiP2P
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
PAYMENTS_TOKEN = os.environ["QIWI_P2P_AUTH_KEY"]
p2p= QiwiP2P(auth_key=PAYMENTS_TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot,storage=MemoryStorage())


