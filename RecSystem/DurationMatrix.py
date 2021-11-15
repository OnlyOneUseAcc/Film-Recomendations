from scipy import sparse
import numpy as np
import pandas as pd

CONTENT_FILE = 'content.csv'
HISTORY_FILE = 'watch_history.csv'
NAME_MATRIX = 'sparse_matrix.npz'


class DurationSparseMatrix:
    def __init__(self, path):
        self.__tables = {'users': dict(),
                         'contents': dict()}
        self.__path = path

    def __read_table(self, name: str):
        index_col = 0 if name == HISTORY_FILE else 'content_uid'
        return pd.read_csv(f'{self.__path}{name}', index_col=index_col)

    def read_info(self):
        history = self.__read_table(HISTORY_FILE)
        self.__tables['users'] = {key: value for key, value in
                                  zip(history.user_uid.unique(), range(len(history.user_uid.unique())))}

        content_df = self.__read_table(CONTENT_FILE)
        self.__tables['contents'] = {key: value for key, value in
                                     zip(content_df.index.values, range(len(content_df.index.values)))}

        return history, content_df

    def create_empty_matrix(self, shape: tuple):
        view_matrix = sparse.lil_matrix(np.zeros(shape))
        self.save_matrix(view_matrix)

    def save_matrix(self, matrix):
        sparse.save_npz(f'{self.__path}{NAME_MATRIX}', matrix.tocsr())

    def load_matrix(self):
        return sparse.load_npz(f'{self.__path}{NAME_MATRIX}').tolil()

    def fill_matrix(self):
        history, content_df = self.read_info()
        view_matrix = self.load_matrix()
        for _, row in history.iterrows():
            view_matrix[self.__tables['users'][row.user_uid], self.__tables['contents'][row.content_uid]] = \
                row.second / content_df.loc[row.content_uid, 'duration_seconds']
        self.save_matrix(view_matrix)

    def get_matrix_part(self, ids: list, ax_type='users'):
        ids = tuple(ids)
        matrix_part = [self.__tables[ax_type][user] for user in ids]
        view_matrix = self.load_matrix()
        lines = view_matrix[matrix_part] if ax_type == 'users' else view_matrix[:, matrix_part]
        return pd.DataFrame(data=lines.toarray(), columns=self.__tables['contents'].keys(), index=ids)

    def get_shape(self):
        len_users = len(self.__tables['users'])
        len_contents = len(self.__tables['contents'])
        return len_users, len_contents