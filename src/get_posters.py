#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io
from bs4 import BeautifulSoup
from urllib import request
import requests
import argparse
from multiprocessing import Pool
import itertools
import utils
import db_manager
import re
from PIL import Image


URL_IMPAWARDS = 'http://www.impawards.com/'
SESSION = requests.Session()

PATH_IMGS = 'data'


def get_title_display(title, year, url):
    version = re.search('_ver([0-9]{2,3}|[2-9])', url)
    if version:
        title_display = '{}, {}, v{}'.format(
            title, year, version.group(1))
    else:
        title_display = '{}, {}'.format(
            title, year)

    return title_display


def get_yearly_url_imgs(year):
    """ Retrieve all the posters' urls along with the title
    from impawards for specific year
    """
    url = '{}{}/std.html'.format(URL_IMPAWARDS,
                                 year)
    r = request.urlopen(url).read()
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
                     'url_img': x}
                    for x, y, z in zip(title_displays,
                                       path_imgs,
                                       path_thumbs)]
        dict_imgs += dict_tmp

    return dict_imgs


def download_poster(link, size_thumb=(50, 50)):
    img_bytes = SESSION.get(link, stream=True, verify=False).content
    file_name = '/'.join(link.split('/')[-3:])
    path_img = '{}/{}'.format(PATH_IMGS, file_name)
    path_thumb = path_img.replace('posters', 'thumbnail')

    img_poster = Image.open(io.BytesIO(img_bytes))
    img_poster.save(path_img)

    img_poster.thumbnail(size_thumb, Image.ANTIALIAS)
    img_poster.save(path_thumb)
    return path_img, path_thumb


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)

    years = range(config['scraping']['years_range'][0],
                  config['scraping']['years_range'][1]+1)
    n_proc = config['scraping']['n_proc']

    print('Retrieve url of posters')
    with Pool(n_proc) as p:
        yearly_urls = p.map(get_yearly_url_imgs, years)
    yearly_urls = list(itertools.chain.from_iterable(yearly_urls))

    for year in years:
        utils.create_folder('{}/{}/posters'.format(PATH_IMGS,
                                                   year))
        utils.create_folder('{}/{}/thumbnails'.format(PATH_IMGS,
                                                      year))

    # push to db
    session = db_manager.get_db(config['general']['db_uri'])
    objects = [db_manager.Poster(x) for x in yearly_urls]

    session.bulk_save_objects(objects)
    session.commit()


if __name__ == "__main__":
    main(sys.argv[1:])
