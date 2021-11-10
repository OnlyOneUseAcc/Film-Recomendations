import numpy as np
import pandas as pd
import scipy.spatial as sp

from RecSystem.MatrixManager import MatrixManager
from RecSystem.DurationMatrix import DurationSparseMatrix
from RecSystem.Exceptions.UserNotFoundException import UserNotFoundException


class Recommendations:

    def __init__(self, path):
        self.__path = path
        self.__mm = MatrixManager(self.__path)

    def get_matrix_manager(self):
        return self.__mm

    def get_rec_by_type(self, type_content: str, count: int = 10, last_history_count: int = 1000):
        top_wh = self.__mm.get_watch_history_table()
        top_wh = top_wh.loc[:last_history_count]
        top_content = top_wh.groupby(['content_uid']).count().sort_values('second', ascending=False).index.tolist()
        content_table = self.__mm.get_content_table()
        film_types = content_table.loc[set(top_content) & set(content_table.index.tolist())]
        return film_types.loc[film_types.type == type_content, ["type", "content_name"]].iloc[: count]

    def top_genres_per_user(self, user_id):
        self.check_user(user_id)
        user_genres = self.__mm.get_user_genre_table_by_user(user_id)
        sort_val = user_genres.sort_values(kind='mergesort', ascending=False)
        top_genres = sort_val[sort_val > 0][:5].index.to_list()

        film_genres = self.__mm.get_film_genre_table()[top_genres]
        history_films = self.__mm.get_watch_history_table()['content_uid']

        history_films = pd.merge(history_films, film_genres, on='content_uid', how='inner').groupby(
            by='content_uid').sum()

        result = {}
        for item in top_genres:
            result[item] = history_films[item].sort_values(
                kind='mergesort', ascending=False).head().index.to_list()

        content = self.__mm.get_content_table()[['content_name', 'type']]
        top_contents = list()
        for item in top_genres:
            for index, row in content.loc[result[item]].iterrows():
                top_content = self.__mm.get_content(index)
                top_contents.extend(top_content)

        return top_contents, top_genres

    def check_user(self, user_id):
        if not self.__mm.user_exist(user_id):
            raise UserNotFoundException(f"User with user_id={user_id} not exist")

    def get_rec_content(self, user_id, num_similar_users):
        self.check_user(user_id)
        user_genres = self.__mm.get_user_genre_table()
        user_content_type = self.__mm.get_user_type_table()
        comb_df = pd.concat([user_content_type, user_genres], axis=1)

        # similarity = comb_df.drop(user_id, axis=0).apply(lambda row: cosine(comb_df.loc[user_id], row), axis=1)
        user = comb_df.loc[user_id].values.reshape((1, comb_df.shape[1]))
        similarity = comb_df.drop(user_id, axis=0)
        similarity = sp.distance.cdist(user, similarity.values, 'cosine')
        users = np.array(comb_df.drop(user_id, axis=0).index.tolist()).reshape((comb_df.shape[0] - 1, 1))
        user_sim = np.hstack([users, similarity.T])
        similarity = pd.DataFrame(data=user_sim, columns=["user_id", "cos_distance"])
        similarity.set_index("user_id", inplace=True)
        similar_users = similarity.sort_values(by=["cos_distance"]).head(num_similar_users).index

        dsm = DurationSparseMatrix(self.__path)
        dsm.read_info()
        user_films = dsm.get_matrix_part(similar_users)

        our_user = dsm.get_matrix_part([user_id])

        dif_films = user_films.apply(lambda row: row - our_user.iloc[0], axis=1)

        top_films = list()

        for col, values in dif_films.iteritems():
            for value in values:
                if value == 1:
                    if col in top_films:
                        continue
                    top_films.append(col)

        return self.__mm.get_content(top_films)


if __name__ == '__main__':
    rec = Recommendations("../Data/")
    print(rec.get_rec_by_type('serial_with_season'))
    print(rec.top_genres_per_user(4))
    print(rec.get_rec_content(4, 1000))
