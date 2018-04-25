import configparser
import os


def read_config(config_path='./config/development.conf'):
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


def create_folder(folder):
    """ Create folders to retrieve posters and thumbnails
    """
    print(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)
