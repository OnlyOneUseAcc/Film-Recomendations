import pandas as pd
from collections.abc import Collection
from models.Content import Content
from models.User import User
from models.WatchHistory import WatchHistory, WatchHistoryUnit


class Table:
    def __init__(self, path):
        self._path = path
        self._columns = self.get_columns()
        self._indexes = self.get_indexes()

    def get_table(self):
        return pd.read_csv(self._path, index_col=0)

    def get_by_uid(self, uid: Collection):
        return self.get_table().loc[uid]

    def remove(self, uid: Collection):
        df_table = self.get_table()
        unique_uids = list(set(self._indexes) & set(uid))
        if len(unique_uids) == 0:
            return

        df_table.drop(unique_uids, inplace=True)
        self._indexes = list(set(self._indexes) - set(unique_uids))
        df_table.to_csv(self._path)

    def get_columns(self):
        with open(self._path, 'r', encoding="utf-8") as file:
            columns = file.readline()

        columns = columns.split(',')[1:]
        return columns

    def get_indexes(self):
        return self.get_table().index.tolist()


class ContentTable(Table):

    def append(self, contents: [Collection, Content]):
        if not isinstance(contents, Collection):
            contents = [contents]

        with open(self._path, 'a') as file:
            for content in contents:
                if content.content_id in self._indexes:
                    continue
                if not isinstance(content.genres, Collection):
                    content.genres = [content.genres]
                genres = f"{','.join(content.genres)}"
                line = f'{content.content_id},{content.name},{content.type},{content.serial_id},"{genres}",{content.duration}\n'
                file.write(line)
                self._indexes.append(content.content_id)


class GenreTable(Table):

    def append(self, film_genres: pd.DataFrame):
        with open(self._path, 'a') as file:

            for index, row in film_genres.iterrows():
                if index in self._indexes:
                    continue
                self._indexes.append(index)
                file.write(f'{index},{",".join([str(value) for value in row.tolist()])}\n')


class UserTypeTable(Table):

    def append(self, user_type: pd.DataFrame):
        with open(self._path, 'a') as file:

            for ind, row in user_type.iterrows():
                if ind in self._indexes:
                    continue
                self._indexes.append(ind)
                file.write(f'{ind},{row.serial_with_season},{row.movie},{row.serial_without_season}\n')


class WatchHistoryTable(Table):

    def remove(self, uf_uid: dict):
        table = self.get_table()
        for user, films in uf_uid.items():
            indexes = table.loc[(table.user_uid == user) & (table.content_uid.isin(films))].index
            table.drop(index=indexes, inplace=True)

        table.to_csv(self._path)

    def append(self, watch_history: WatchHistory):
        cur_index = max(self._indexes) + 1

        with open(self._path, 'a') as file:
            for content in watch_history.history:
                self._indexes.append(cur_index)
                file.write(f'{cur_index},{content.user_uid},{content.content_uid},{content.duration}\n')
                cur_index += 1

    def get_by_user_id(self, user_id):
        data = self.get_table()
        return data[data['user_uid'] == user_id]


class UserTable(Table):

    def append(self, user: User):
        with open(self._path, 'a') as file:
            if user.id in self._indexes:
                return False

            line = f'{user.id},{user.name},{user.password},{str(user.is_admin)}\n'
            file.write(line)
            self._indexes.append(user.id)

        return True


def test_UserTable():
    ids = [10000, 0]
    userT = User(id=ids[0], name='Nikita', is_admin=False, password=1234)
    userF = User(id=ids[1], name='Nikita', is_admin=False, password=1234)

    ut = UserTable(path='../Data/users.csv')

    T = ut.append(userT)
    F = ut.append(userF)
    print(f'True|{T}, False|{F}')

    if T and F:
        ut.remove(ids)
    elif T and not F:
        ut.remove([ids[0]])
    elif not T and F:
        ut.remove([ids[1]])


def test_WatchHistoryTable():
    wht = WatchHistoryTable(path='../Data/watch_history.csv')

    unit1 = WatchHistoryUnit(user_uid=0, content_uid=12, name='Qwerty', duration=6500, type=None)
    unit2 = WatchHistoryUnit(user_uid=0, content_uid=11, name='werty', duration=16500, type='serial')

    wh = WatchHistory(history=[unit1, unit2])
    print(f'Part 1: Full constructor: {wh.history}')

    wh = WatchHistory(history=[unit1])
    print(f'Part 2: One construct: {wh.history}')
    wh.append(unit2)
    print(f'Part 2: Append: {wh.history}')

    wh = WatchHistory(history=None)
    print(f'Part 3: Zero construct: {wh.history}')
    wh.append(unit2)
    print(f'Part 3: Append: {wh.history}')
    wh.append(unit1)
    print(f'Part 3: Append: {wh.history}')

    print(f'Part 4: Indexes Before: {len(wht.get_indexes())}')
    wht.append(wh)
    print(f'Part 4: Indexes After appending: {len(wht.get_indexes())}')
    wht.remove({0: [11, 12]})
    print(f'Part 4: Indexes After removing : {len(wht.get_indexes())}')


def test_UserTypeTable():
    pass


def test_GenreTable():
    pass


def test_ContentTable():
    pass


if __name__ == '__main__':
    print('UserTable test:')
    test_UserTable()
    print('=' * 30)
    print('WatchHistoryTable test:')
    test_WatchHistoryTable()
    print('=' * 30)
