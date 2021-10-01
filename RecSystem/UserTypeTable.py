import pandas as pd
from collections.abc import Collection


class UserTypeTable:

    def __init__(self, path: str):
        self.__path = path

    def get_types_by_users(self, user_id: Collection):
        return pd.read_csv(self.__path, index_col=0).loc[user_id]

    def append_new_user_type(self, user_type: pd.DataFrame):
        with open(self.__path, 'a') as file:
            for ind, row in user_type.iterrows():
                file.write(f'{ind},{row.serial_with_season},{row.movie},{row.serial_without_season}\n')

    def remove_user_type(self, users: Collection):
        df_user_type = pd.read_csv(self.__path, index_col=0)
        df_user_type.drop(index=users, inplace=True)
        df_user_type.to_csv(self.__path)


if __name__ == '__main__':
    row = pd.Series(data=[999999, 0, 2222, 1111], index=['index', 'serial_with_season', 'movie', 'serial_without_season'])
    print(row.index)
    ut = pd.DataFrame(data=[row], index=[row.values[0]], columns=row.index.values[1:])
    print(ut)
    utt = UserTypeTable('../Data/user_content_types.csv')
    utt.append_new_user_type(ut)
    print(utt.get_types_by_users([999999]))
    utt.remove_user_type([999999])
