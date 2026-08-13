import logging
from create_bot import dp, bot, p2p
from aiogram import types
from aiogram.types.message import ContentType
from datetime import datetime
from handlers.other import PSql
from random import randint
from keyborad import client_kb
from memberships import check_membership
import datetime

logging.basicConfig(level=logging.INFO)


@dp.message_handler(lambda message: 'Купить подписку' in message.text)
async def bot_mess(message: types.Message):
    data_now = str(datetime.datetime.now())[:10].split('-')
    data_old = await check_membership.info_memmber(message.from_user.id)
    if datetime.date(int(data_now[0]),int(data_now[1]),int(data_now[2]))>datetime.date(int(data_old[0]),int(data_old[1]),int(data_old[2])):
        comment = str(message.from_user.id) + "_" + str(randint(1000, 9999))
        bill = p2p.bill(amount=150, lifetime=10, comment=comment)
        await PSql(user=message.from_user.id).add_check(bill.bill_id)

        await bot.send_message(message.from_user.id, f"Вам выставлен счёт.",
                           reply_markup=client_kb.buy_menu(url=bill.pay_url, bill=bill.bill_id))
    else:
        await bot.send_message(message.from_user.id, f"У вас имеется подписка до:\n {data_old[0]}-{data_old[1]}-{data_old[2]}.",)



@dp.callback_query_handler(text_contains='check_')
async def check(callback: types.CallbackQuery):
    bill = str(callback.data)[6:]
    # print(bill)
    info = await PSql().get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == 'PAID':
            data = str(datetime.datetime.now())[:10].split('-')
            if data[1] == '12':
                data[1] = '01'
                data[0] = str(int(data[0]) + 1)
            data_1 = '-'.join(data)
            await PSql(user=callback.from_user.id, membership=data_1).update_membership()
            await PSql().delete_check(bill_id=bill)
            await bot.send_message(callback.from_user.id, 'Счёт успешно оплачен☺️')
        else:
            await bot.send_message(callback.from_user.id, 'Вы не оплатили счёт.',
                                   reply_markup=client_kb.buy_menu(False, bill=bill))

    else:
        await bot.send_message(callback.from_user.id, 'Счёт не найден.')
