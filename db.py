import string
import requests
from psycopg2 import connect as db_connect, sql
from random import randint as rnd, choice
from datetime import date


words = requests.get('https://www.randomlists.com/data/words.json').json().get('data')


def create_value(value_type):
    if value_type == 'name':
        return choice(words)

    elif value_type == 'phone':
        return f'+7 {rnd(100, 999)} {rnd(100, 999)} {rnd(10, 99)} {rnd(10, 99)}'

    elif value_type == 'date':
        srt = date.today().replace(day=1, month=1).toordinal()
        end = date.today().toordinal()
        random_day = date.fromordinal(rnd(srt, end))
        return random_day.strftime('%d.%m.%Y')

    elif value_type == 'email':
        result = ''
        for i in range(rnd(8, 20)):
            result += choice(string.ascii_letters)
        return result + '@mail.ru'

    else:
        return None


# Есть база данных, содержащая таблицу “объектов”
class DB:
    def __init__(self):
        self.__connection = db_connect(dbname='postgres', user='postgres', password='89206142018BOB', host='localhost')

    def execute(self, query):
        try:
            with self.__connection:
                with self.__connection.cursor() as cursor:
                    sql_query = sql.SQL(query)
                    cursor.execute(sql_query)
                    data = cursor.fetchall()
                    return data
        except:
            return 'error'

    def fill(self, len_items):
        # В рамках реализации задачи можно добавлять любое количество дополнительных полей
        object_types = ['phone', 'date', 'email']
        folders = [0]
        for i in range(1, len_items + 1):
            if rnd(0, 3):
                object_type = choice(object_types)
                # Каждый объект обязательно имеет не пустые поля id (число) и name (строка)
                object_tuple = i, create_value("name"), choice(folders), object_type, create_value(object_type)
            else:
                # Объект типа "папка" может содержать в себе (логически) другие объекты (посредством связи
                # потомок-родитель)
                object_tuple = i, create_value("name"), choice(folders), "folder", ""
                folders.append(i)
            self.execute(f"INSERT INTO objects (id, name, parent, type, value) VALUES {object_tuple}")


if __name__ == '__main__':
    db = DB()
    db.fill(1000)
