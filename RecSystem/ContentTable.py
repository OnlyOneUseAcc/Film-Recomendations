from collections.abc import Collection

import pandas as pd
from models.Content import Content

CONTENT_PATH = '../Data/content.csv'


class ContentTable:
    def __init__(self, path: str = CONTENT_PATH):
        self.__content_path = path

    def get_info_content(self, content_uid: Collection):
        df_content = pd.read_csv(self.__content_path, index_col=0)
        return df_content.loc[content_uid]

    def append_info_content(self, contents: [Collection, Content]):
        if not isinstance(contents, Collection):
            contents = [contents]
        with open(self.__content_path, 'a') as file:
            for content in contents:
                if not isinstance(content.genres, Collection):
                    content.genres = [content.genres]
                genres = f"{','.join(content.genres)}"
                line = f'{content.content_id},{content.name},{content.type},{content.serial_id},"{genres}",{content.duration}\n'
                file.write(line)

    def get_serialized_info(self, content_uid):
        df_content = self.get_info_content(content_uid)

        content_collection = []
        for ind, row in df_content.iterrows():
            content = Content(content_id=ind, name=row.content_name, type=row.type, serial_id=row.serial_id,
                              genres=row.genres.split(','), duration=row.duration_seconds)
            content_collection.append(content)

        return content_collection


if __name__ == '__main__':
    ct = ContentTable()

    new_content1 = Content(content_id=123, name='Somebody1', type='serial', serial_id=20010, genres=['toon', 'music'],
                           duration=80000)
    new_content2 = Content(content_id=124, name='Somebody2', type='serial', serial_id=20010, genres=['toon', 'music'],
                           duration=80000)
    new_content3 = Content(content_id=125, name='Somebody3', type='serial', serial_id=20010, genres=['toon', 'music'],
                           duration=80000)

    ct.append_info_content([new_content3, new_content2, new_content1])
    print(new_content3.__dict__)
    print(ct.get_serialized_info([123, 124, 125]))
