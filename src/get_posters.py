#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from bs4 import BeautifulSoup
from urllib import request
import argparse
from subprocess import DEVNULL, STDOUT, check_call, call
from multiprocessing import Pool
import itertools
from functools import partial
import utils
import db_manager


URL_IMPAWARDS = 'http://www.impawards.com/'


def get_yearly_url_imgs(year):
    """ Retrieve all the posters' urls along with the title
    from impawards for specific year
    """
    url = '{}{}/std.html'.format(URL_IMPAWARDS,
                                 year)
    r = request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html5lib')

    # Find all trs
    trs = soup.find_all('tr')

    dict_imgs = []
    format_url = '{base}{year}/posters/{link}'
    for tr in trs[::2]:
        tds = tr.find_all('td')
        title = tds[0].text
        html_links = [x.get('href') for x in tds[1].find_all('a')]
        url_imgs = [format_url.format(base=URL_IMPAWARDS,
                                      year=year,
                                      link=x)
                    for x in html_links]
        dict_tmp = [{'title': title,
                     'year': year,
                     'url_img': x.replace('html', 'jpg')}
                    for x in url_imgs]
        dict_imgs += dict_tmp

    return dict_imgs


def download_poster(link, config):
    poster_folder = config['scraping']['folder_images']
    thumb_folder = config['scraping']['folder_thumbnails']
    img_file = link['url_img'].split('/')[-1]
    folder = '{}/{}/'.format(poster_folder, link['year'])
    check_call(['wget', '-P', folder, link['url_img']],
               stdout=DEVNULL, stderr=STDOUT)

    path_img = '{}{}'.format(folder, img_file)
    path_thumb = '{}/{}/{}'.format(thumb_folder,
                                   link['year'],
                                   img_file)
    str_system = 'convert {} -resize 50x50! {}'.format(
        path_img, path_thumb)
    call(str_system, shell=True)
    link['path_img'] = path_img
    link['path_thumb'] = path_thumb
    return link


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args['config'])

    years = range(config['scraping']['years_range'][0],
                  config['scraping']['years_range'][1]+1)
    n_proc = config['scraping']['n_proc']

    print('Creating folders for posters and thumbnails')

    folder_posters = config['scraping']['folder_images']
    folder_thumbs = config['scraping']['folder_thumbnails']
    folders_to_create = [folder_posters, folder_thumbs]
    folders_to_create += [os.path.join(folder_posters, str(x))
                          for x in years]
    folders_to_create += [os.path.join(folder_thumbs, str(x))
                          for x in years]

    [utils.create_folder(folder) for folder in folders_to_create]

    print('Retrieve url of posters')
    yearly_urls = [get_yearly_url_imgs(x)
                   for x in years]
    yearly_urls = list(itertools.chain.from_iterable(yearly_urls))

    print('Downloading posters')
    with Pool(n_proc) as p:
        data_download = p.map(partial(download_poster, config=config),
                              yearly_urls)

    # push to db
    session = db_manager.get_db(config['general']['db_uri'])
    objects = [db_manager.Poster(x) for x in data_download]

    session.bulk_save_objects(objects)
    session.commit()


if __name__ == "__main__":
    main(sys.argv[1:])
