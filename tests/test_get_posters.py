# -*- coding: utf-8 -*-

import sys
import unittest

from src.get_posters import (download_poster, get_title_display,
                             get_yearly_url_imgs)

sys.path.append('src')


class UtilsGetPosters(unittest.TestCase):
    def setUp(self):
        self.year = 1913
        self.dict_imgs_1913 = get_yearly_url_imgs(1913)

    def test_get_yearly_url_imgs(self):
        dict_imgs_1913 = self.dict_imgs_1913

        self.assertTrue(isinstance(
            dict_imgs_1913, list))

        self.assertTrue(all(
            [isinstance(x, dict) for x in dict_imgs_1913]))

        self.assertTrue(all(
            ['title' in x.keys() for x in dict_imgs_1913]))

        self.assertTrue(all(
            ['year' in x.keys() for x in dict_imgs_1913]))

        self.assertTrue(all(
            ['title_display' in x.keys() for x in dict_imgs_1913]))

        self.assertTrue(all(
            ['base64_img' in x.keys() for x in dict_imgs_1913]))

        self.assertTrue(all(
            ['base64_thumb' in x.keys() for x in dict_imgs_1913]))

        self.assertTrue(all(
            ['url_img' in x.keys() for x in dict_imgs_1913]))

    def test_download_poster(self):
        link = self.dict_imgs_1913[0]
        img, thumb = download_poster(link['url_img'], size_thumb=(50, 50))
        self.assertTrue(isinstance(img, str))
        self.assertTrue(isinstance(thumb, str))

    def test_get_title_display(self):
        title = 'my movie title'
        year = 2010
        url1 = 'http://dummyurl.com/2010/posters/my_movie_title.jpg'
        url2 = 'http://dummyurl.com/2010/posters/my_movie_title_ver2.jpg'
        url3 = 'http://dummyurl.com/2010/posters/my_movie_title_ver28.jpg'

        title_display1 = get_title_display(title, year, url1)
        title_display2 = get_title_display(title, year, url2)
        title_display3 = get_title_display(title, year, url3)
        self.assertTrue(
            title_display1 == 'my movie title, 2010')
        self.assertTrue(
            title_display2 == 'my movie title, 2010, v2')
        self.assertTrue(
            title_display3 == 'my movie title, 2010, v28')
