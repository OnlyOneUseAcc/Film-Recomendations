import pandas as pd
import numpy as np

FILM_GENRE_PATH = '../Data/film_genres.csv'


class FilmGenreTable:

    def __init__(self, path: str = FILM_GENRE_PATH):
        self.__content_path = path

    def update_table(self, film_genres: pd.DataFrame):
        df_film_genres = pd.read_csv(self.__content_path, index_col='content_uid')

        for index, row in film_genres.iterrows():
            if index in df_film_genres.index:
                continue
            else:
                columns = set(row.index) & set(df_film_genres.columns)

                if len(columns) == 0:
                    continue

                df_film_genres.loc[index] = 0
                df_film_genres.loc[index, columns] = 1

    def get_table(self):
        return pd.read_csv(self.__content_path, index_col='content_uid')
