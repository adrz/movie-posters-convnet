#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import sys

import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

import db_manager
import utils
from db_manager import Poster


def scale_coords(coords: np.array, width: int=800, height: int=800) -> list:
    """ Scale the coordinates to fit within a specific range

    Parameters
    ----------
    coords (np.array or list): coordinates to be scaled
    width (int): width limit
    height (int): height limit

    Returns:
    scaled (list): list of coordinates all in $[0, width]x[0, height]$
    """
    minx, miny = min(coords[:, 0]), min(coords[:, 1])
    maxx, maxy = max(coords[:, 0]), max(coords[:, 1])

    scale_x = width / (maxx - minx)
    scale_y = height / (maxy - miny)

    scaled = [[(x[0] - minx) * scale_x,
               (x[1] - miny) * scale_y]
              for x in coords]
    return scaled


def get_pca_features(data: list, n_components: int) -> np.array:
    """ Dimensional reduction of the features
    """
    features = np.array([x.features for x in data])
    pca = PCA(n_components=n_components, whiten=True)
    X = pca.fit_transform(features)
    return X


# Function getting the closest 6 movie posters for all the movie posters
# Far from being a beautiful code...
def get_closest_features(data: list, db, config):
    """ Compute PCA and use cosine_similarity to compute "distance"
    between each posters
    """
    X = get_pca_features(data, config['features']['pca_n_components'])

    # Could become HUGE !
    # Don't forget that cosine_similarity will compute a NxN matrix
    # with N as the number of posters
    X_cosine = cosine_similarity(X)

    # Diagonal values of X_cosine are 1s (a poster is of course identical to itself)
    # As we are looking for the closest posters except itself, we set the diagonal values to 0s
    np.fill_diagonal(X_cosine, 0)

    # The largest the cosine similarity, the closest the features are
    idx_bests = np.argsort(X_cosine)
    idx_bests = idx_bests[:, ::-1]
    idx_keep = idx_bests[:, 0:6]

    # Push the data to db
    for d, idxs in zip(data, idx_keep):
        ids = [data[j].id for j in idxs]
        d.closest_posters = ','.join(map(str, ids))
        # x = db.query(Poster).filter_by(id=d.id).first()
        # x.closest_posters = closest_posters

    db.commit()
    return True


def get_2d_features(data, db, config):
    """ Uniform Manifold Approximation and Projection
    see: https://arxiv.org/abs/1802.03426
    """
    import umap
    features = np.array([x.features for x in data])
    embedding = umap.UMAP(n_neighbors=30,
                          min_dist=0.3, n_components=500,
                          metric='cosine').fit_transform(features)
    embedding = np.array(scale_coords(embedding, width=1024, height=500))
    for d, f in zip(data, embedding):
        d.features_pca = f
    db.commit()
    return True


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)

    db = db_manager.get_db(config['general']['db_uri'])

    data = db.query(Poster).all()

    _ = get_2d_features(data, db, config)
    _ = get_closest_features(data, db, config)



if __name__ == "__main__":
    main(sys.argv[1:])
