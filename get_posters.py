#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from urllib import request
import pandas as pd
import os
import pickle
import sys
import argparse
from subprocess import DEVNULL, STDOUT, check_call


# Create folders to receive posters and thumbnails
def create_folder(folder):
    print(folder)
    if not os.path.exists(folder):
        os.makedirs(folder)


# Scrap the url of posters from 'impawards.com/'
def get_url_imgs(url_start, year):

    url = url_start+str(year)+'/std.html'
    r = request.urlopen(url).read()
    soup = BeautifulSoup(r)

    # Find all ahrefs
    links = soup.find_all('a')

    # Filter first useless links
    links_filter = [links[i] for i in range(53, len(links)-1)]
    links_filter = list(map(lambda x: x.get('href'), links_filter))

    # Pandas easier for text-processing
    df = pd.DataFrame({'html_link': links_filter})
    # df['html_link'] = df['html_link'].str.replace('_ver[0-9]+','')
    df.drop_duplicates(inplace=True)
    df['year'] = year
    df['url_imgs'] = url_start + str(year) + '/posters/' + \
                     df.html_link.str.replace('.html', '.jpg')

    return df


def download_posters(df, convert_location):
    local_image = []
    local_thumb = []

    for index, row in df.iterrows():
        folder = './posters/'+str(row['year']) + '/'

        # Download poster with wget
        check_call(['wget', '-P', folder, row['url_imgs']],
                   stdout=DEVNULL, stderr=STDOUT)
        file_str = folder + row['url_imgs'].split('/')[-1]
        local_image.append(file_str)
        thumbnail_file = './thumbs/' + str(row['year']) + '/' + \
                         row['url_imgs'].split('/')[-1]

        # Downsample posters to a 50x50 pixels (for datavisualization purpose)
        str_system = convert_location + ' ' + file_str + \
                     ' -resize 50x50! ' + thumbnail_file
        os.system(str_system)
        local_thumb.append(thumbnail_file)

    df['local_image'] = local_image
    df['local_thumb'] = local_thumb
    return df


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--range',
                        help="range of years to scrap (ex: 1920-2017)",
                        default="1990-2017")
    parser.add_argument('-o', '--output_file',
                        help="output pickle file used to locate posters file",
                        default='./cnn_posters.p')
    parser.add_argument('-c', '--convert_location',
                        help="location of ImageMagick convert",
                        default='convert')
    args = parser.parse_args()

    first_year = int(args.range.split('-')[0])
    last_year = int(args.range.split('-')[1])

    years = range(first_year, last_year+1)

    print('Creating folders for posters and thumbnails')
    folders_to_create = ['./posters/', './thumbs/']
    folders_to_create += map(lambda x: './posters/'+str(x), years)
    folders_to_create += map(lambda x: './thumbs/'+str(x), years)
    [create_folder(folder) for folder in folders_to_create]

    print('Retrieve url of posters')
    url_start = 'http://www.impawards.com/'
    df_list = list(map(lambda x: get_url_imgs(url_start, x), years))
    df = pd.concat(df_list, ignore_index=True)

    print('Downloading posters')
    df = download_posters(df, args.convert_location)
    pickle.dump(df, open(args.output_file, 'wb'))

    print('Scraping Finished')


if __name__ == "__main__":
    main(sys.argv[1:])
