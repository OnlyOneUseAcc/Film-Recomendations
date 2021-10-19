import pandas as pd

from Table import *
from models.Content import Content
from models.WatchHistory import WatchHistory
from models.User import User
import hashlib


class MatrixManager:
    def __init__(self, path: str):
        self.__content_table = ContentTable(f'{path}/content.csv')
        self.__film_genres_table = ContentTable(f'{path}/film_genres.csv')
        self.__users_genres_table = ContentTable(f'{path}/users_genres.csv')
        self.__user_type_table = ContentTable(f'{path}/user_content_types.csv')
        self.__watch_history_table = ContentTable(f'{path}/watch_history.csv')
        self.__user_table = UserTable(f'{path}/users.csv')

    def get_content(self, content_id):

        df_content = self.__content_table.get_by_uid(content_id)

        content_collection = []
        for ind, row in df_content.iterrows():
            content = Content(content_id=ind, name=row.content_name, type=row.type, serial_id=row.serial_id,
                              genres=row.genres.split(','), duration=row.duration_seconds)
            content_collection.append(content)

        return content_collection

    def user_exist(self, id: int, password: str):
        user = self.__user_table.get_by_uid([id])

        if user is None:
            return None
        elif user.iloc[0].password == password:
            user = user.iloc[0]
            return User(id=int(user.name),
                        name=str(user.user_name),
                        is_admin=bool(user.is_admin),
                        password=str(user.password))
        else:
            return None

    def insert_content(self, content: Content):
        self.__content_table.append(content)

    def insert_watch_history(self, history: WatchHistory):
        exist_content_history = list()
        content_uids = self.__content_table.get_indexes()
        for history_unit in history.history:
            if history_unit.content_uid in content_uids:
                exist_content_history.append(history_unit)
        self.__watch_history_table.append(WatchHistory(history=exist_content_history))

    def insert_user(self, user: User):
        return self.__user_table.append(user)

    def get_watch_history(self, user_id: int):
        return self.__watch_history_table.get_by_uid([user_id])


if __name__ == '__main__':
    mm = MatrixManager(path='../Data')
    print(mm.insert_user(User(id=0, name='Nikita', is_admin=True, password='parol')))
    print(mm.user_exist(0, 'parol'))
