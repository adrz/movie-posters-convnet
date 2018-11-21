# -*- coding: utf-8 -*-

import configparser
import os


def read_config(config_path: str='./config/development.conf') -> dict:
    """ Extract configuration from a file

    Parameters
    ----------
    config_path (str): local path to the configuration file

    Returns
    ----------
    config (dict): dictionary with the configuration
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_path)

    # convert
    config = config._sections

    # scraping
    config['scraping']['years_range'] = (
        [int(x) for x in config['scraping']['years_range'].split('-')])
    config['scraping']['n_proc'] = int(config['scraping']['n_proc'])

    config['features']['pca_n_components'] = int(config['features']
                                                 ['pca_n_components'])
    return config


def create_folder(folder: str):
    """ Create folders to retrieve posters and thumbnails

    Parameters
    ----------
    folder (str): local path of the folder to be created
    """
    print(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
