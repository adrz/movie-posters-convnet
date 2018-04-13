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
import urllib
from multiprocessing import Pool
import json

def get_imdb_link(url):
    try:
        r = request.urlopen(url).read()
        soup = BeautifulSoup(r)
        all_link = soup.find_all('a')
        imdb_link = list(filter(lambda x: 'imdb.com/' in x['href'], all_link))[0]['href']
        title = soup.find('h3').text
    except:
        imdb_link = ''
        title = ''

    print(imdb_link)
    return (imdb_link, title)


def get_omdb_api(url):
    print(url)
    try:
        r = request.urlopen(url).read().decode()
        to_return = json.loads(r)
    except:
        to_return = []
    return to_return



def put_imdb(df, data_movies):
    df['imdbID'] = list(map(lambda x: x[0], data_movies))
    df['imdbID'] = df['imdbID'].str.extract('(tt[0-9]+)')
    df['title'] = list(map(lambda x: x[1], data_movies))
    return df


def clean_imdb_data(df):
    df['imdbVotes'] = df.imdbVotes.str.replace(',','')
    df.loc[df.imdbVotes=='N/A','imdbVotes'] = 0
    df['imdbVotes'] = df['imdbVotes'].astype(int)

    df['Year'] = df['Year'].astype(int)
    df.loc[df.imdbRating=='N/A', 'imdbRating'] = 0
    df['imdbRating'] = df['imdbRating'].astype(float)
    # df['Runtime'] = df['Runtime'].str.replace('N/A','0')
    # df['Runtime'] = df['Runtime'].str.replace(' min', '') 
    # df['Runtime'] = df.Runtime.astype(int)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file',
                        help='input file with urls of posters',
                        default='./cnn_posters.p')
    parser.add_argument('-o', '--output_file',
                       help='output pickle file',
                       default='./cnn_posters_imdb.p')
    parser.add_argument('-n', '--nproc', type=int,
                        help="number of processus (default 2)",
                        default=2)
    args = parser.parse_args()
    nproc = args.nproc

    df = pickle.load(open(args.input_file,'rb'))

    urls = 'http://www.impawards.com/' + df.year.astype(str) + '/' + df.html_link
    print('Retrieve imdb link from imposter')
    with Pool(nproc) as p:
        data_imdb = p.map(get_imdb_link,urls)

    imdb_links = list(map(lambda x: x[0], data_imdb))
    titles = list(map(lambda x: x[1], data_imdb))
    df['imdb_link'] = imdb_links
    df['title'] = titles

    df = df[df.imdb_link!=''].reset_index()

    imdb_links = pd.Series(df.imdb_link.unique())
    imdb_links = imdb_links.str.replace('http://www.imdb.com/title/', 'http://www.omdbapi.com/?i=')
    print('Retrieve imdb data from omdbapi')
    with Pool(nproc) as p:
        data_omdb = p.map(get_omdb_api, list(imdb_links))

    data_omdb_filter = list(filter(lambda x: len(x), data_omdb))
    df_imdb = pd.DataFrame(data_omdb_filter)

    df['imdbID'] = df.imdb_link.str.extract('(tt[0-9]+)')

    df = pd.merge(df, df_imdb, on='imdbID')
    pickle.dump(df, open(args.output_file, 'wb'))

if __name__ == "__main__":
    main(sys.argv[1:])
