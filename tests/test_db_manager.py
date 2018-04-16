import unittest
from src.db_manager import (Base, ARRAY, Poster, get_db, get_all_data)
import numpy as np
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm.session import Session


class DbManagerTest(unittest.TestCase):
    def setUp(self):
        self.uri_db = 'sqlite:///tests/data/movie_posters.db'

    def test_ARRAY(self):
        myArr = ARRAY()
        self.assertTrue(isinstance(myArr, TypeDecorator))

    def test_Poster(self):
        poster = Poster()
        self.assertTrue(isinstance(
            poster, Base))

        dict_poster = {'title': 'mytitle',
                       'url_img': 'http://dumdum.com',
                       'path_img': './data/img.jpg',
                       'path_thumb': './data/img.thumb',
                       'features': np.array([1, 2, 3]),
                       'features_pca': np.array([1, 2]),
                       'closest_posters': '',
                       'title_display': 'dfs'}
        poster_b = Poster(dict_poster)

        dict_poster_b = poster_b.__dict__
        del(dict_poster_b['_sa_instance_state'])

        self.assertTrue(dict_poster_b == dict_poster)

    def test_read_write_Poster(self):
        db = get_db('sqlite://')
        dict_poster = {'title': 'mytitle',
                       'url_img': 'http://dumdum.com',
                       'path_img': './data/img.jpg',
                       'path_thumb': './data/img.thumb',
                       'features': np.array([1, 2, 3]),
                       'features_pca': np.array([1, 2]),
                       'closest_posters': '',
                       'title_display': 'dfs'}
        new_poster = Poster(dict_poster)
        # in memory test
        db.add(new_poster)

        poster_tmp = db.query(Poster).all()[0]
        self.assertTrue(new_poster == poster_tmp)
        self.assertTrue(all(poster_tmp.features == dict_poster['features']))

    def test_get_db(self):
        db = get_db(self.uri_db)
        self.assertTrue(isinstance(db, Session))

    # def test_get_all_data(self):
    #     data, db = get_all_data(self.uri_db)
    #     self.assertTrue(len(data) == 2)

    #     self.assertTrue((data[0].title ==
    #                      'Alias Jimmy Valentine'))
