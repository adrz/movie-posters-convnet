import unittest
import os
import sys
sys.path.append('src')
from src.get_posters import (get_yearly_url_imgs,
                             download_poster, get_title_display)
from src.utils import create_folder
import shutil


class UtilsGetPosters(unittest.TestCase):
    def setUp(self):
        self.year = 1933
        self.dict_imgs_1933 = get_yearly_url_imgs(1933)

    def test_get_yearly_url_imgs(self):
        dict_imgs_1933 = self.dict_imgs_1933

        self.assertTrue(isinstance(
            dict_imgs_1933, list))

        self.assertTrue(all(
            [isinstance(x, dict) for x in dict_imgs_1933]))

        self.assertTrue(all(
            ['title' in x.keys() for x in dict_imgs_1933]))

        self.assertTrue(all(
            ['url_img' in x.keys() for x in dict_imgs_1933]))

    def test_download_poster(self):
        link = self.dict_imgs_1933[0]
        year = link['year']
        config = dict()
        config['scraping'] = {'folder_images': './tmp/p',
                              'folder_thumbnails': './tmp/t'}
        create_folder('./tmp/p/{}'.format(year))
        create_folder('./tmp/t/{}'.format(year))
        link_download = download_poster(link, config)

        self.assertTrue(
            'path_img' in link_download.keys())
        self.assertTrue(
            'path_thumb' in link_download.keys())

        self.assertTrue(
            os.path.exists(link_download['path_img']))
        self.assertTrue(
            os.path.exists(link_download['path_thumb']))

        shutil.rmtree('tmp/')

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
