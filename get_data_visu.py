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


def process_features(df, pca_components, perplexity,
                     n_jobs, output_file, tsne_alg):
    pca = PCA(n_components=pca_components, whiten=True)

    if tsne_alg == 'sklearn':
        tsne = TSNE(n_components=2, perplexity=perplexity)
    else:
        tsne = TSNE_multi(n_components=2, perplexity=perplexity, n_jobs=n_jobs)

    data = np.array(list(df['features']))

    data = pca.fit_transform(data)
    data_tsne = tsne.fit_transform(data)
    scaled_data = scale_coords(data_tsne, width=800, height=800)
    scaled_data_array = np.array(scaled_data)
    df['features_visu_x'] = scaled_data_array[:,0]
    df['features_visu_y'] = scaled_data_array[:,1]
    return df
#    json.dump(df_json.values.tolist(),
#              open(output_file, 'w'))

def get_json_autocomplete(df, output):

    output = 'datasets/data_autocomplete_all.json'
    df_json = df[['title', 'url_imgs', \
                'closest_1', 'closest_2','closest_3', 'closest_4', 'closest_5', 'closest_6',\
                'score_1','score_2','score_3','score_4','score_5','score_6']]
    df_json.to_json(output,  orient='records')





def get_closest_features_bis(df, pca_components):
    # df_min = df[~df.local_image.str.contains('_ver[2-9]')]
    # df_min = df_min[~df_min.local_image.str.contains('_ver[0-9][0-9]')]

    pca_components = 10000
    features = np.array(list(df['features']))
    # features = np.array(list(df['features_chollet']))
    pca = PCA(n_components=pca_components, whiten=True)
    X = pca.fit_transform(features)

    ## Could become HUGE !
    X_cosine = cosine_similarity(X)

    np.fill_diagonal(X_cosine, 0)
    score_1 = []
    score_2 = []
    score_3 = []
    score_4 = []
    score_5 = []
    score_6 = []


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


    # for idx, row in df.iterrows():
    #     row_cosine = X_cosine[idx,:]
    #     idx_best = np.argsort(row_cosine)[::-1][0:3]
    #     # df.loc[idx,'closest_1'] = df.iloc[idx_best[0]]['url_imgs']
    #     # df.loc[idx,'closest_2'] = df.iloc[idx_best[1]]['url_imgs']
    #     # df.loc[idx,'closest_3'] = df.iloc[idx_best[2]]['url_imgs']
    #     # df.loc[idx,'score_1'] = row_cosine[idx_best[0]]
    #     # df.loc[idx,'score_2'] = row_cosine[idx_best[1]]
    #     # df.loc[idx,'score_3'] = row_cosine[idx_best[2]]

    #     closest_1.append(df.iloc[idx_best[0]]['url_imgs'])
    #     closest_2.append(df.iloc[idx_best[1]]['url_imgs'])
    #     closest_3.append(df.iloc[idx_best[2]]['url_imgs'])
    #     score_1.append(row_cosine[idx_best[0]])
    #     score_2.append(row_cosine[idx_best[1]])
    #     score_3.append(row_cosine[idx_best[2]])

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

    max_score = df['score_1'].max()
    min_score = df['score_1'].min()
    df['score_1'] = ((df['score_1'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_2'] = ((df['score_2'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_3'] = ((df['score_3'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_4'] = ((df['score_4'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_5'] = ((df['score_5'] - min_score)/(max_score-min_score)*100).astype('int')
    df['score_6'] = ((df['score_6'] - min_score)/(max_score-min_score)*100).astype('int')

    return df




# def get_closest_features(df, pca_components):
#     #df_min = df[~df.local_image.str.contains('_ver[2-9]')]
#     #df_min = df_min[~df_min.local_image.str.contains('_ver[0-9][0-9]')]

#     pca_components = 500
#     features = np.array(list(df['features']))
#     pca = PCA(n_components=pca_components, whiten=True)
#     X = pca.fit_transform(features)
#     X_cosine = cosine_similarity(X)
#     np.fill_diagonal(X_cosine, 0)
#     df['closest_1'] = ''
#     df['closest_2'] = ''
#     df['closest_3'] = ''
#     df['score_1'] = ''
#     df['score_2'] = ''
#     df['score_3'] = ''

#     closest_1 = []
#     closest_2 = []
#     closest_3 = []
#     score_1 = []
#     score_2 = []
#     score_3 = []
#     # df.reset_index(inplace=True)
#     for idx, row in df.iterrows():
#         row_cosine = X_cosine[idx,:]
#         idx_best = np.argsort(row_cosine)[::-1][0:3]

#         closest_1.append(df.iloc[idx_best[0]]['local_image'])
#         closest_2.append(df.iloc[idx_best[1]]['local_image'])
#         closest_3.append(df.iloc[idx_best[2]]['local_image'])
#         score_1.append(row_cosine[idx_best[0]])
#         score_2.append(row_cosine[idx_best[1]])
#         score_3.append(row_cosine[idx_best[2]])       


#         # df.loc[idx,'closest_1'] = df.iloc[idx_best[0]]['local_image']
#         # df.loc[idx,'closest_2'] = df.iloc[idx_best[1]]['local_image']
#         # df.loc[idx,'closest_3'] = df.iloc[idx_best[2]]['local_image']
#         # df.loc[idx,'score_1'] = row_cosine[idx_best[0]]
#         # df.loc[idx,'score_2'] = row_cosine[idx_best[1]]
#         # df.loc[idx,'score_3'] = row_cosine[idx_best[2]]

#     df['closest_1'] = closest_1
#     df['closest_2'] = closest_2
#     df['closest_3'] = closest_3

#     df['score_1'] = score_1
#     df['score_2'] = score_2
#     df['score_3'] = score_3

#     max_score = df['score_1'].max()
#     min_score = df['score_1'].min()
#     df['score_1'] = ((df['score_1'] - min_score)/(max_score-min_score)*100).astype('int')
#     df['score_2'] = ((df['score_2'] - min_score)/(max_score-min_score)*100).astype('int')
#     df['score_3'] = ((df['score_3'] - min_score)/(max_score-min_score)*100).astype('int')
#     return df


    
def write_output_json(df, output_file):

    # Scale score
    df_json = df[(df.score_1 > 45) & (df.score_1 < 70)]
    df_json = df.sample(2000)


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

    output_file = 'datasets/x_200_200.json'
    df_json = df_json[['features_visu_x', 'features_visu_y',\
                  'local_thumb', 'url_imgs',\
                  'closest_1', 'closest_2', 'closest_3', \
                  'closest_4', 'closest_5', 'closest_6', \
                  'score_1','score_2','score_3']]
    json.dump(df_json.values.tolist(),
              open(output_file, 'w'))
    

def filter_df(df, n_sample):
    df = df[df['features'].apply(len) == 4096]
    df_min = df[~df.local_image.str.contains('_ver[2-9]')]
    df_min = df_min[~df_min.local_image.str.contains('_ver[0-9][0-9]')]
    df_min = df_min.sample(n_sample)
    return df_min


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
                        type=int, default=500)
    parser.add_argument('-p', '--perplexity',
                        help="perplexity for TSNE",
                        type=int, default=30)
    parser.add_argument('-j', '--n_jobs',
                        help="number of cores to use for the tsne",
                        type=int, default=4)
    parser.add_argument('-t', '--tsne',
                        help='implementation tsne (multicore/sklearn)',
                        default='sklearn')
    parser.add_argument('-s', '--n_sample',
                        help='number of sample selected for visualization',
                        type=int, default=4000)
    args = parser.parse_args()

    df = pickle.load(open(args.input_file, 'rb'))

    df['ver'] = df.html_link.str.extract('_ver([0-9]{2,3}|[2-9])').fillna('1')
    newtitle = df.title.str.replace('(',', ') \
                       .str.replace(')','')
    newtitle = newtitle + ' , ' + 'ver ' + df['ver']
    df['title'] = newtitle

    df = filter_df(df, args.n_sample)
    df = process_features(df, args.pca_components,
                     args.perplexity,
                          args.n_jobs, args.output_file, args.tsne)
    df = get_closest_features(df, 500)
    write_output_json(df, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
