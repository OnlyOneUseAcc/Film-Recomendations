import unittest

import pandas as pd

from RecSystem import Table
from models import User, Content


class TestTables(unittest.TestCase):
    ut = Table.UserTable('../Data/users.csv')
    wht = Table.WatchHistoryTable('../Data/watch_history.csv')
    gt = Table.GenreTable('../Data/film_genres.csv')
    ct = Table.ContentTable('../Data/content.csv')
    utt = Table.UserTypeTable('../Data/user_content_types.csv')

    def test_append_UserTable(self):
        """
        Checks if UserTable.append() can append user and throws False if user with the same idx exists
        """
        user = User.User(id=1, name='Vasya', is_admin=False, password=1234)
        self.ut.append(user)
        table = pd.read_csv('../Data/users.csv')
        true_last_row = {'id': {0: 1}, 'user_name': {0: 'Vasya'}, 'password': {0: 1234}, 'is_admin': {0: False}}
        result_last_row = table.tail(1).to_dict()

        self.assertEqual(true_last_row, result_last_row)
        self.assertEqual(False, self.ut.append(user))

    def test_append_WatchHistoryTable(self):
        """
        Checks if WatchHistoryTable.append() can append watch history unit
        """
        pass

    def test_append_UserTypeTable(self):
        """
        Checks if UserTypeTable.append() can append user type
        """
        pass

    def test_appendContentTable(self):
        """
        Checks if ContentTable.append() can append Content
        """
        content = Content.Content(content_id=1488, name='Zeleniy Slonik', type='movie', serial_id=None,
                                  genres=['drama'],
                                  duration=7200)
        self.ct.append(content)
        table = pd.read_csv('../Data/content.csv')
        true_last_row = {'content_name': {3829: 'Zeleniy Slonik'},
                         'content_uid': {3829: 1488},
                         'duration_seconds': {3829: 7200.0},
                         'genres': {3829: 'drama'},
                         'serial_id': {3829: 'None'},
                         'type': {3829: 'movie'}}

        result_last_row = table.tail(1).to_dict()

        self.assertEqual(true_last_row, result_last_row)


if __name__ == '__main__':
    unittest.main()
