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


# Scaling function
def scale_coords(coords, width=800, height=800):
    minx = min(coords[:, 0])
    miny = min(coords[:, 1])
    maxx = max(coords[:, 0])
    maxy = max(coords[:, 1])

    scale_x = width / (maxx - minx)
    scale_y = height / (maxy - miny)
    print(scale_x, scale_y, minx, miny, maxx, maxy)
    scaled = []
    for i in range(coords.shape[0]):
        x = coords[i, 0]
        y = coords[i, 1]
        scaled.append([(x - minx) * scale_x, (y - miny) * scale_y])
    return scaled


# def process_features(df, pca_components, perplexity,
#                      n_jobs, output_file, tsne_alg):
#     pca = PCA(n_components=pca_components, whiten=True)

#     if tsne_alg == 'sklearn':
#         tsne = TSNE(n_components=2, perplexity=perplexity)
#     else:
#         tsne = TSNE_multi(n_components=2, perplexity=perplexity, n_jobs=n_jobs)

#     data = np.array(list(df['features']))

#     data = pca.fit_transform(data)
#     data_tsne = tsne.fit_transform(data)
#     scaled_data = scale_coords(data_tsne, width=800, height=800)
#     scaled_data_array = np.array(scaled_data)
#     df['features_visu_x'] = scaled_data_array[:,0]
#     df['features_visu_y'] = scaled_data_array[:,1]
#     return df
#    json.dump(df_json.values.tolist(),
#              open(output_file, 'w'))


# Function to output the data use by the search engine
def get_json_search_engine(df, output):
    df_json = df[['title', 'url_imgs', \
                'closest_1', 'closest_2','closest_3', 'closest_4', 'closest_5', 'closest_6',\
                'score_1','score_2','score_3','score_4','score_5','score_6']]
    df_json.to_json(output,  orient='records')




# Function getting the closest 6 movie posters for all the movie posters
# Far from being a beautiful code...
def get_closest_features(df, pca_components):
    features = np.array(list(df['features']))
    pca = PCA(n_components=pca_components, whiten=True)
    X = pca.fit_transform(features)

    ## Could become HUGE !
    X_cosine = cosine_similarity(X)

    np.fill_diagonal(X_cosine, 0)
    score_1, score_2, score_3, \
        score_4, score_5, score_6 = [],[],[],[],[],[]

    # The largest the cosine similarity, the closest the features are
    idx_bests = np.argsort(X_cosine)
    idx_bests = idx_bests[:,::-1]
    idx_keep = idx_bests[:,0:6]

    closest_1 = list(df.iloc[idx_keep[:,0]].url_imgs)
    closest_2 = list(df.iloc[idx_keep[:,1]].url_imgs)
    closest_3 = list(df.iloc[idx_keep[:,2]].url_imgs)
    closest_4 = list(df.iloc[idx_keep[:,3]].url_imgs)
    closest_5 = list(df.iloc[idx_keep[:,4]].url_imgs)
    closest_6 = list(df.iloc[idx_keep[:,5]].url_imgs)

    for idx in range(idx_keep.shape[0]):
        row_cosine = X_cosine[idx,:]
        score_1.append(row_cosine[idx_keep[idx,0]])
        score_2.append(row_cosine[idx_keep[idx,1]])
        score_3.append(row_cosine[idx_keep[idx,2]])
        score_4.append(row_cosine[idx_keep[idx,3]])
        score_5.append(row_cosine[idx_keep[idx,4]])
        score_6.append(row_cosine[idx_keep[idx,5]])

    df['closest_1'] = closest_1
    df['closest_2'] = closest_2
    df['closest_3'] = closest_3
    df['closest_4'] = closest_4
    df['closest_5'] = closest_5
    df['closest_6'] = closest_6

    df['score_1'] = score_1
    df['score_2'] = score_2
    df['score_3'] = score_3
    df['score_4'] = score_4
    df['score_5'] = score_5
    df['score_6'] = score_6

    # Normalize scores to fit between 0 and 100
    max_score = df['score_1'].max()
    min_score = df['score_1'].min()
    df['score_1'] = ((df['score_1'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_2'] = ((df['score_2'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_3'] = ((df['score_3'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_4'] = ((df['score_4'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_5'] = ((df['score_5'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_6'] = ((df['score_6'] - min_score)/(max_score-min_score)*100).astype('int')
    return df

    
def process_features_tsne(df, n_samples=2000, perplexity=40, n_jobs=2, output_file, tsne_alg='sklearn'):
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

    df_json = df_json[['features_visu_x', 'features_visu_y',\
                  'local_thumb', 'url_imgs',\
                  'closest_1', 'closest_2', 'closest_3', \
                  'closest_4', 'closest_5', 'closest_6', \
                  'score_1','score_2','score_3']]
    json.dump(df_json.values.tolist(),
              open(output_file, 'w'))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file',
                        help="input file (output of get_features_from_cnn.py)",
                        default="./cnn_posters_features.p")
    parser.add_argument('-o', '--output_file',
                        help="output json file used by d3js",
                        default='./datasets/x.json')
    parser.add_argument('-n', '--pca_components',
                        help="number of PCA components for data reduction",
                        type=int, default=200)
    parser.add_argument('-p', '--perplexity',
                        help="perplexity for t-SNE",
                        type=int, default=30)
    parser.add_argument('-j', '--n_jobs',
                        help="number of cores to use for the tsne",
                        type=int, default=4)
    parser.add_argument('-t', '--tsne',
                        help='implementation tsne (multicore/sklearn)',
                        default='sklearn')
    parser.add_argument('-s', '--n_sample',
                        help='number of sample selected for visualization',
                        type=int, default=2000)
    args = parser.parse_args()

    df = pickle.load(open(args.input_file, 'rb'))

    # Get the version of the posters and update title accordingly
    df['ver'] = df.html_link.str.extract('_ver([0-9]{2,3}|[2-9])').fillna('1')
    newtitle = df.title.str.replace('(',', ') \
                       .str.replace(')','')
    newtitle = newtitle + ' , ' + 'ver ' + df['ver']
    df['title'] = newtitle

    # Search Engine 
    df = get_closest_features(df, args.pca_components)
    output = 'datasets/data_autocomplete_all.json'
    get_json_search_engine(df, output)
    # t-SNE 2D features
    process_features_tsne(df, args.pca_components,
                     args.perplexity,
                          args.n_jobs, args.output_file, args.tsne)
    
    write_output_json(df, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
