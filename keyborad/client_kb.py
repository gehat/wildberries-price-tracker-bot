from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton('➕ Добавить товар')
b2 = KeyboardButton('☑ Список отслежываемых товаров')
b3 = KeyboardButton('ℹ Помощь')
b4 = KeyboardButton('🚫 Очистить отслеживаемое')
b5=KeyboardButton('💰 Купить подписку')

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Отмена 💥', callback_data='answer'))

pay = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Купить подписку💥', callback_data='buy'))

kb_klient = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_klient.add(b1).insert(b2).add(b3).insert(b4).insert(b5)


def buy_menu(isUrl=True, url='', bill=''):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text='Ссылка на оплату.', url=url)
        qiwiMenu.insert(btnUrlQIWI)

    btnCheckQIWI = InlineKeyboardButton(text='Проверить оплату.', callback_data='check_' + bill)
    qiwiMenu.insert(btnCheckQIWI)

    return qiwiMenu