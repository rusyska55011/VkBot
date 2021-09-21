import sqlite3
from dotenv import dotenv_values
import vk_api
from vk_api.utils import get_random_id


class DataBase:
    db_name = 'ClientBase.db'

    def __init__(self, table_name, cols, key_col_name):
        self.table_name = table_name
        self.cols = cols
        self.cols_names = self.__get_cols_names(self.cols)
        self.key = key_col_name

        self.db = sqlite3.connect(self.db_name)
        self.create_table()

    @staticmethod
    def __get_cols_names(cols) -> str:
        cols_list = cols.split(',')
        cols_names_list = [item.split()[0] for item in cols_list]
        return ', '.join(cols_names_list)

    def connect(func):
        def wrapper(self, *args, **kwargs):
            cursor = self.db.cursor()
            returned = func(self, cursor, *args, **kwargs)
            self.db.commit()
            return returned
        return wrapper

    @connect
    def create_table(self, cursor):
        def __do_key(cols, key_col_name) -> str:
            querys = list()
            for item in cols.split(','):
                if key_col_name in item:
                    item += ' PRIMARY KEY'
                querys.append(item.strip())
            return ', '.join(querys)

        cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} ({__do_key(self.cols, self.key)})')

    @connect
    def add(self, cursor, *args: list):
        for arg in args:
            arg = tuple(map(lambda item: str(item), arg))
            arg = '"' + '", "'.join(arg) + '"'
            try:
                cursor.execute(f'INSERT INTO {self.table_name} ({self.cols_names}) VALUES ({arg});')
            except sqlite3.IntegrityError:
                print(f'Добавление {arg} невозможно. Элемент с данным ID уже существует')

    @connect
    def delete(self, cursor, *args: int):
        for arg in args:
            cursor.execute(f'DELETE FROM {self.table_name} WHERE {self.key} = {str(arg)}')

    @connect
    def read(self, cursor) -> list:
        return cursor.execute(f'SELECT * FROM {self.table_name}').fetchall()

    def get_col_names(self) -> str:
        return self.cols

    def open_db(self):
        self.db = sqlite3.connect(self.db_name)

    def close_db(self):
        self.db.close()


class VkBase(DataBase):
    def __init__(self):
        super().__init__(table_name='vk', cols='vk_id INT, name TEXT', key_col_name='vk_id')


class VkBot:
    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id

        self.vk = vk_api.VkApi(token=access_token)
        self.base = VkBase()

    def __send_message(self, vk_id, message):
        self.vk.method('messages.send', {
            'user_id': vk_id,
            'message': message,
            'random_id': get_random_id()
        })

    def push_messages(self, message):
        base_items = self.base.read()
        for vk_id, name in base_items:
            self.__send_message(vk_id, message)


access_token, user_id = dotenv_values('.env').values()

vk = VkBot(access_token=access_token, user_id=user_id)
vk.push_messages('11')