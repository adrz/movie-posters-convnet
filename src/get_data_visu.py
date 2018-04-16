#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as TSNE_multi
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import pandas as pd
import numpy as np
import json
import sys
import os
import pickle
import argparse

import utils
import db_manager


def scale_coords(coords, width=800, height=800):
    """ Scale the coordinate to fit within a specific range
    """
    minx = min(coords[:, 0])
    miny = min(coords[:, 1])
    maxx = max(coords[:, 0])
    maxy = max(coords[:, 1])

    scale_x = width / (maxx - minx)
    scale_y = height / (maxy - miny)

    scaled = [[(x[0] - minx) * scale_x,
               (x[1] - min_y) * scale_y]
              for x in coords]
    return scaled


def get_PCA_features(data, n_components):
    features = np.array([x.features for x in data])
    pca = PCA(n_components=n_components, whiten=True)
    X = pca.fit_transform(features)
    return X


# Function getting the closest 6 movie posters for all the movie posters
# Far from being a beautiful code...
def get_closest_features(data, db, config):
    X = get_PCA_features(data, config['features']['pca_n_components'])

    # Could become HUGE !
    X_cosine = cosine_similarity(X)

    np.fill_diagonal(X_cosine, 0)

    # The largest the cosine similarity, the closest the features are
    idx_bests = np.argsort(X_cosine)
    idx_bests = idx_bests[:, ::-1]
    idx_keep = idx_bests[:, 0:6]

    closest_urls = []
    for d, idxs in zip(data, idx_keep):
        # d.closest_posters = ';'.join([data[x].url_img for x in idxs])
        d.closest_posters = ','.join(idxs+1)

    db.commit()


def process_features_tsne(df, n_samples=2000,
                          perplexity=40, n_jobs=2,
                          output_file, tsne_alg='sklearn'):
    df_json = df.sample(n_samples)

    # n_components fixed to 200
    pca = PCA(n_components=200, whiten=True)

    if tsne_alg == 'sklearn':
        tsne = TSNE(n_components=2, perplexity=perplexity)
    else:
        tsne = TSNE_multi(n_components=2, perplexity=perplexity, n_jobs=n_jobs)

    data = np.array(list(df_json['features']))

    data = pca.fit_transform(data)
    data_tsne = tsne.fit_transform(data)

    scaled_data = scale_coords(data_tsne, width=1000, height=1000)
    scaled_data_array = np.array(scaled_data)
    df_json['features_visu_x'] = scaled_data_array[:,0]
    df_json['features_visu_y'] = scaled_data_array[:,1]

    df_json = df_json[['features_visu_x', 'features_visu_y',
                       'local_thumb', 'url_imgs',
                       'closest_1', 'closest_2', 'closest_3',
                       'closest_4', 'closest_5', 'closest_6',
                       'score_1', 'score_2', 'score_3']]
    json.dump(df_json.values.tolist(),
              open(output_file, 'w'))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)
    data, db = db_manager.get_all_data(config['general']['db_uri'])

    data_features = get_closest_features(data, db, config)
    db.commit()


if __name__ == "__main__":
    main(sys.argv[1:])
