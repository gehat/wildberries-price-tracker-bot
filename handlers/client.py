from aiogram import types, Dispatcher
import pay_and_scrapping.payments
from create_bot import dp,bot
from keyborad.client_kb import kb_klient
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from pay_and_scrapping.wb import Browsr
from handlers.other import PSql
from keyborad.client_kb import inkb
from memberships.check_membership import check_member


class FSMClien(StatesGroup):
    url = State()


async def start(message: types.Message):
    user_full = message.from_user.full_name
    await message.answer(
        f'Привет, {user_full}.\n'
        f'Чтобы начать отслеживание нажми на кнопку "Добавить товар".\n'
        f'После этого бот вам сообщит как цена на товар упадёт.\n'
        f'Помните, добавить можно только тот товар, который имеет цену в данный момент!\n'
        f'Без подписки можно добавить только 1 товар.Но всего лишь за 150 ₽, можно будет довать не ограниченное колличество товаров.\n',
        reply_markup=kb_klient)
    await PSql(user=message.from_user.id,start='True').update_membership()


async def help_message(message: types.Message):
    await message.answer(
        f'Данный бот отслеживает цену добавленного вами товара, на площадке Wildberries.'
        f'Чтобы начать, скиньте боту ссылку на товар, и когда цена на товаре упадёт, бот вам сообщит.\n'
        f'"Покупая подписку вы помогаете развитию проекта и быстродействию ответа сервера ☺️"',
        reply_markup=kb_klient)


@dp.message_handler(lambda message: 'Добавить товар' in message.text, state=None)
async def added_product(message: types.Message):
    if await check_member(message.from_user.id):
        await FSMClien.url.set()
        await message.answer('Вставьте ссылку на товар.', reply_markup=inkb)
    else:
        await message.answer('Увы без подписки вы не можете следить более чем за 1 товаром.\n'
                             'Приобретите подписку чтобы снять данное ограничение.',reply_markup=kb_klient)



@dp.callback_query_handler(text_startswith='answer', state=FSMClien.url)
async def und(cal: types.CallbackQuery, state=FSMClien.url):
    call_data = cal.data
    await cal.message.answer('Действие отменено.', reply_markup=kb_klient)
    await cal.answer()
    await state.finish()

@dp.callback_query_handler(text_startswith='buy')
async def und(cal: types.CallbackQuery):
    call_data = cal.data
    await pay_and_scrapping.payments.bot_mess(cal.from_user.id)

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    data = callback_query.data.split('  ')
    await PSql(query=f"DELETE FROM users WHERE idd={int(data[2])} and user_id={int(data[1])}",user=int(data[1])).update_or_delete()
    await callback_query.answer('Запись удалена', show_alert=True)
    await callback_query.message.delete()
    await callback_query.answer()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('update  '))
async def del_callback_run(callback_query: types.CallbackQuery):
    data = callback_query.data.split('  ')
    await PSql(
        query=f'UPDATE users SET price={int(data[3])} WHERE idd={int(data[2])} and user_id={int(data[1])}').update_or_delete()
    await callback_query.answer('Следим дальше)', show_alert=True)
    await callback_query.message.delete()
    await callback_query.answer()


@dp.message_handler(state=FSMClien.url)
async def url_add(message: types.Message, state: FSMContext):
    await PSql(user=message.from_user.id).trial()
    user_id = message.from_user.id
    data = await Browsr(message.text, user_id).get_elements
    await PSql(data[0], data[1], data[2], data[3]).insert()
    await message.answer('Отслеживание успешно добавлено.', reply_markup=kb_klient)
    await state.finish()

async def check_product(message: types.Message):
    user_id = message.from_user.id
    await PSql(user_id).products_list()


async def unsubscribe(message: types.Message):
    user_id = message.from_user.id
    await PSql(user_id).unsubscrd()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help_message, lambda message: 'Помощь' in message.text)
    dp.register_message_handler(check_product, lambda message: 'Список отслежываемых товаров' in message.text)
    dp.register_message_handler(unsubscribe, lambda message: 'Очистить отслеживаемое' in message.text)
    dp.register_message_handler(pay_and_scrapping.payments.bot_mess,lambda message: 'Купить подписку' in message.text)