import collections

import pandas as pd

from RecSystem.Table import *
from models.Content import Content
from models.User import User
from models.WatchHistory import WatchHistory


class MatrixManager:
    def __init__(self, path: str):
        self.__content_table = ContentTable(f'{path}/content.csv')
        self.__film_genres_table = GenreTable(f'{path}/film_genres.csv')
        self.__users_genres_table = GenreTable(f'{path}/users_genres.csv')
        self.__user_type_table = UserTypeTable(f'{path}/user_content_types.csv')
        self.__watch_history_table = WatchHistoryTable(f'{path}/watch_history.csv')
        self.__user_table = UserTable(f'{path}/users.csv')

    def get_content(self, content_id):

        if not isinstance(content_id, collections.Sequence):
            content_id = [content_id]
        df_content = self.__content_table.get_by_uid(content_id)
        if type(df_content) is pd.Series:
            df_content = df_content.to_frame().transpose()

        content_collection = []
        for ind, row in df_content.iterrows():
            serial_id = -1
            type_content = ""
            genres = ""
            if not pd.isna(row.serial_id):
                serial_id = row.serial_id
            if not pd.isna(row.type):
                type_content = row.type
            if not pd.isna(row.genres):
                genres = row.genres

            content = Content(content_id=ind, name=row.content_name, type=type_content, serial_id=serial_id,
                              genres=genres.split(','), duration=row.duration_seconds)
            content_collection.append(content)

        return content_collection

    def user_exist(self, user_id: int):
        if int(user_id) < 0:
            return False
        else:
            user_info = self.__user_table.get_indexes()
            return int(user_id) in user_info

    def get_user_info(self, id: int, password: str):
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
        units = []
        for item in self.__watch_history_table.get_by_user_id(user_id).values:
            content = self.get_content(item[1])
            unit = WatchHistoryUnit(user_uid=item[0],
                                    content_uid=item[1],
                                    duration=item[2] / content[0].duration,
                                    name=content[0].name,
                                    type=content[0].type)
            units.append(unit)
        history = WatchHistory(history=units)
        return history

    def get_user_genre_table_by_user(self, user_id):
        return self.__users_genres_table.get_by_uid(user_id)

    def get_film_genre_table(self):
        return self.__film_genres_table.get_table()

    def get_watch_history_table(self):
        return self.__watch_history_table.get_table()

    def get_user_type_table(self):
        return self.__user_type_table.get_table()

    def get_content_table(self):
        return self.__content_table.get_table()

    def get_user_genre_table(self):
        return self.__users_genres_table.get_table()


if __name__ == '__main__':
    mm = MatrixManager(path='../Data')
    print(mm.insert_user(User(id=0, name='Nikita', is_admin=True, password='parol')))
    print(mm.user_exist(0, 'parol'))
