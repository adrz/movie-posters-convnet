#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import io
import itertools
import re
import sys
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup
from PIL import Image

import db_manager
import utils

URL_IMPAWARDS = 'http://www.impawards.com/'
SESSION = requests.Session()

PATH_IMGS = 'data'


def get_title_display(title: str, year: int, url: str) -> str:
    """
    Extract simplified title.

    Parameters
    ----------
    title (str): movie title
    year (int): date of the movie
    url (str): url of the movie poster

    Returns
    ----------
    title_display (str): format "title, year, version"
    """

    version = re.search('_ver([0-9]{2,3}|[2-9])', url)
    if version:
        title_display = '{}, {}, v{}'.format(
            title, year, version.group(1))
    else:
        title_display = '{}, {}'.format(
            title, year)

    return title_display


def get_yearly_url_imgs(year: int) -> list:
    """
    Retrieve all the posters' urls along with the title
    from impawards for specific year

    Parameters
    ----------
    year (int): date format %Y (eg 1990)

    Returns
    ----------
    dict_imgs (list): list of dictionary containing information related to the movies.
    """

    url = '{}{}/std.html'.format(URL_IMPAWARDS,
                                 year)
    # r = request.urlopen(url).read()
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'lxml')

    # Find all trs
    trs = soup.find_all('tr')

    dict_imgs = []
    format_url = '{base}{year}/posters/{link}'
    for itr, tr in enumerate(trs[::2]):
        tds = tr.find_all('td')
        title = tds[0].text
        html_links = [x.get('href') for x in tds[1].find_all('a')]
        url_imgs = [format_url.format(base=URL_IMPAWARDS,
                                      year=year,
                                      link=x)
                    for x in html_links]
        url_imgs = [x.replace('html', 'jpg') for x in url_imgs]
        paths = [download_poster(x) for x in url_imgs]
        path_imgs = [x[0] for x in paths]
        path_thumbs = [x[1] for x in paths]
        title_displays = [get_title_display(title, year, x) for x in url_imgs]
        dict_tmp = [{'title': title,
                     'year': year,
                     'path_img': x,
                     'path_thumb': y,
                     'title_display': z,
                     'url_img': w}
                    for x, y, z, w in zip(path_imgs,
                                          path_thumbs,
                                          title_displays,
                                          url_imgs)]
        dict_imgs += dict_tmp

    return dict_imgs


def download_poster(link: str, size_thumb: tuple=(100, 100)) -> tuple:
    """
    Download the poster and create a thumbnail

    Parameters
    ----------
    link (str): url of the poster
    size_thumb (tuple): dimension of the thumbnail

    Returns
    ----------
    path_img (str): local path of the downloaded poster
    path_thumb (str): local path of the thumbnail
    """
    img_bytes = SESSION.get(link, stream=True, verify=False).content
    file_name = '/'.join(link.split('/')[-3:])
    path_img = '{}/{}'.format(PATH_IMGS, file_name)
    path_thumb = path_img.replace('posters', 'thumbnails')

    img_poster = Image.open(io.BytesIO(img_bytes))
    img_poster.save(path_img)

    img_poster.thumbnail(size_thumb, Image.ANTIALIAS)
    img_poster.save(path_thumb)
    return path_img, path_thumb


def main(argv):
    # arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)

    years = range(config['scraping']['years_range'][0],
                  config['scraping']['years_range'][1]+1)
    n_proc = config['scraping']['n_proc']

    # create the folders in which the poster will be downloaded
    for year in years:
        utils.create_folder('{}/{}/posters'.format(PATH_IMGS,
                                                   year))
        utils.create_folder('{}/{}/thumbnails'.format(PATH_IMGS,
                                                      year))

    # Downloading the posters with multiprocessing (highly speed up compare to single process)
    print('Retrieve url of posters')
    with Pool(n_proc) as p:
        yearly_urls = p.map(get_yearly_url_imgs, years)
    yearly_urls = list(itertools.chain.from_iterable(yearly_urls))

    # push to db
    session = db_manager.get_db(config['general']['db_uri'])
    objects = [db_manager.Poster(x) for x in yearly_urls]
    session.bulk_save_objects(objects)
    session.commit()


if __name__ == "__main__":
    main(sys.argv[1:])
