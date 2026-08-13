import psycopg2
from pay_and_scrapping import wb
from create_bot import bot
import asyncio
from keyborad.client_kb import kb_klient
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from random import randint
from aiogram.utils.exceptions import BotBlocked


class PSql():  # inicialization data user
    def __init__(self, user: int = None, name: str = None, url: str = None, price: int = None, query: str = None,
                 membership: str = None, start: str = None):
        self.__user = user
        self.name = name  # name product
        self.url = url
        self.price = price
        self.__con = None
        self.query = query
        self.membership = membership
        self.start = start

    async def connect(self):  # connect your psql databse
        try:
            self.__con = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="111",
                host="127.0.0.1",
                port="5432"
            )
            print("Database opened successfully")

        except:
            print('Error opening database')

    async def insert(self):  # insert into your database
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(
            f"INSERT INTO USERS (user_id,name_product,url,price) VALUES ({self.__user},'{self.name}', '{self.url}',{self.price})"
        )

        self.__con.commit()
        print("Record inserted successfully")

        self.__con.close()
        print('Data base is close')

    async def search(self):  # automatic price scanning
        while True:
            await asyncio.sleep(15000)
            print(f'Starting check price reduction\n {datetime.now()}')
            await self.connect()
            cur = self.__con.cursor()
            cur.execute('SELECT user_id,name_product,url,price,idd FROM USERS')
            rows = cur.fetchall()
            for row in rows:
                client = await wb.Browsr(row[2]).get_elements # Browse class get url
                if client[1] is not None and client[3] is not None and client[3] < row[
                    3]:  # Comparison of the old price from the database and the new one received
                    user = row[
                        0]  # data[0]{self.__user},data[1]'{self.name}', data[2]'{self.url}',data[3]{self.price}
                    try:
                        await bot.send_message(chat_id=user,
                                               text=f'Цена на товар упала:\n "{row[1]}"\n Старая цена: {row[3]}₽\n Новая '
                                                    f'цена: {client[3]}₽\n Ссылка на твоар: {row[2]}',
                                               reply_markup=InlineKeyboardMarkup(). \
                                               add(InlineKeyboardButton(f'Удалить',
                                                                        callback_data=f'del  {user}  {row[4]}')))
                                                   #InlineKeyboardButton(f'Следить дальше',
                                                                       # callback_data=f'update  {user}  {row[4]}  {client[3]}')))
                        cur.execute(f'UPDATE users SET price={client[3]} WHERE idd={row[4]} and user_id={row[0]}')
                        self.__con.commit()
                    except BotBlocked:
                        pass
                elif client[3] is None:  # if the price of the product is not specified
                    print(f'Товара:{client[1]}     | нет в наличии')
                    continue

            self.__con.close()
            print(f'Data base is close, searching ended {datetime.now()}')

    async def products_list(self):  # Output of products added by the user
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(f'SELECT name_product,url,price,idd FROM USERS WHERE user_id={self.__user}')
        row = cur.fetchall()
        if (len(row)) == 0:
            await bot.send_message(chat_id=self.__user, text='Вы ещё не добавили ни одного товара',
                                   reply_markup=kb_klient)
        for row in row:
            await asyncio.sleep(randint(0, 1))
            await bot.send_message(chat_id=self.__user, text=f'{row[0]}\nЦена: {row[2]}\n{row[1]}',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'Удалить', callback_data=f'del  {self.__user}  {row[3]}')))
        self.__con.close()
        print('Data base is close')

    async def unsubscrd(self):  # Delete user data
        await self.connect()
        cur = self.__con.cursor()
        print(self.__user)
        cur.execute(f'DELETE FROM users WHERE user_id={self.__user}')
        self.__con.commit()

        cur.execute(f'SELECT * FROM memberships WHERE user_id={self.__user}')
        row = cur.fetchall()
        if len(row) != 0 and row[0][2] == 'Trial':
            cur.execute(
                f"UPDATE memberships SET membership='False'")
            self.__con.commit()

        await bot.send_message(chat_id=self.__user, text='Товары успешно удалены.', reply_markup=kb_klient)
        print('Data base is close')
        self.__con.close()

    async def update_or_delete(self):
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(self.query)
        self.__con.commit()
        if 'DELETE' in self.query:
            cur.execute(f'SELECT * FROM memberships WHERE user_id={self.__user}')
            row = cur.fetchall()
            if len(row) != 0 and row[0][2] == 'Trial':
                cur.execute(
                    f"UPDATE memberships SET membership='False'")
                self.__con.commit()

        print('Data base is close')
        self.__con.close()

    async def update_membership(self):
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(f'SELECT * FROM memberships WHERE user_id={self.__user}')
        row = cur.fetchall()
        if len(row) == 0 and self.start == 'True':
            cur.execute(f"INSERT INTO memberships VALUES ({self.__user},'False', 'Trial')")
        elif self.start == 'True' and len(row) != 0:
            print(f'Пользователь {self.__user} уже есть в базе данных')
        elif len(row) == 0:
            cur.execute(f"INSERT INTO memberships VALUES ({self.__user},'True', '{self.membership}')")
        else:
            cur.execute(
                f"UPDATE memberships SET membership='True', data_payment='{self.membership}' WHERE user_id={self.__user}")

        self.__con.commit()
        self.__con.close()
        print('SUCEESS!')

    async def trial(self):
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(f'SELECT * FROM memberships WHERE user_id={self.__user}')
        row = cur.fetchall()
        if row[0][2] == 'Trial':
            cur.execute(
                f"UPDATE memberships SET membership='True', data_payment='Trial' WHERE user_id={self.__user}")

            self.__con.commit()

        self.__con.close()

    async def add_check(self, bill_id):
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(f"INSERT INTO checkk (user_id,bill_id) VALUES({self.__user},'{bill_id}')")
        self.__con.commit()
        self.__con.close()

    async def get_check(self, bill_id):
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(f"SELECT * FROM checkk WHERE bill_id='{bill_id}'")
        row = cur.fetchall()
        self.__con.close()
        if (len(row)) == 0:
            return False
        else:
            return True

    async def delete_check(self, bill_id):
        await self.connect()
        cur = self.__con.cursor()
        cur.execute(f"DELETE FROM checkk WHERE bill_id ='{bill_id}'")
        self.__con.commit()
        self.__con.close()
