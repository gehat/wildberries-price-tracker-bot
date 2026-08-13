import asyncio
import psycopg2
import datetime


async def check_member(user_id):
    connect = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="111",
        host="127.0.0.1",
        port="5432"
    )
    cur = connect.cursor()
    cur.execute(f'SELECT * FROM memberships WHERE user_id={user_id}')
    row = cur.fetchall()
    data_now = str(datetime.datetime.now())[:10].split('-')
    data_old = row[0][2].split('-')
    print(data_old)
    print(data_now)
    if data_old[0] == 'Admin' or data_old[0] == 'Trial' and row[0][1] == 'False':
        return True
    if data_old[0] == 'Trial' and row[0][1] == 'True':
        return False
    if datetime.date(int(data_now[0]), int(data_now[1]), int(data_now[2])) < datetime.date(int(data_old[0]),
                                                                                           int(data_old[1]),
                                                                                           int(data_old[2])):
        return True
    else:
        return False


async def info_memmber(user_id):
    connect = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="111",
        host="127.0.0.1",
        port="5432"
    )
    cur = connect.cursor()
    cur.execute(f'SELECT * FROM memberships WHERE user_id={user_id}')
    row = cur.fetchall()
    data = row[0][2].split('-')
    if data[0] == 'Admin':
        return ['2030','12','22']
    elif data[0]=='Trial':
        return ['1998','12','22']
    else:
        return data
