import unittest
from src.utils import (read_config, create_folder)
import os


class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.config_path = 'config/development.conf'

    def test_read_conf(self):
        config = read_config(self.config_path)
        sections = [x for x in config.keys()]
        for x in ['general', 'scraping']:
            with self.subTest(x=x):
                self.assertTrue(x in sections)

        # test general sections
        subsections = [x for x in config['general'].keys()]
        for x in ['db_uri']:
            with self.subTest(x=x):
                self.assertTrue(x in subsections)

        # test scraping sections
        subsections = [x for x in config['scraping'].keys()]
        for x in ['years_range', 'folder_images',
                  'folder_thumbnails', 'converter', 'n_proc']:
            with self.subTest(x=x):
                self.assertTrue(x in subsections)

        self.assertTrue(isinstance(
            config['scraping']['years_range'], list))

        self.assertTrue(isinstance(
            config['scraping']['n_proc'], int))

        self.assertTrue(
            len(config['scraping']['years_range']) == 2)

    def test_create_folder(self):
        folder_tmp = './dummy-folder'
        create_folder(folder_tmp)
        self.assertTrue(os.path.exists(folder_tmp))
        os.rmdir(folder_tmp)
