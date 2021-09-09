import pandas as pd

CONTENT_PATH = '../Data/content.csv'
COLUMNS_NAME = ['name', 'type', 'serial_id', 'genres', 'duration_seconds']


class ContentTable:

    def __init__(self, path: str = CONTENT_PATH):
        self.__content_path = path

    def get_info_content(self, content_uid):
        df_content = pd.read_csv(self.__content_path, index_col=0)

        if isinstance(content_uid, int):
            content_uid = [content_uid]

        return df_content.loc[content_uid]

    def append_info_content(self, info_content: pd.DataFrame):
        df_content = pd.read_csv(self.__content_path, index_col=0)

        for index, row in info_content.iterrows():
            if len(set(row.index) - set(COLUMNS_NAME)) != 0:
                continue
            df_content.loc[index] = row

        df_content.to_csv(self.__content_path)
