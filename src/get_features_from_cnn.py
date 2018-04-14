#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from cnnkeras import *

import sys
import argparse
import numpy as np
from functools import reduce
from operator import mul

from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.vgg16 import VGG16

import utils
import db_manager


# Variable specific to vgg-16/vgg-19
img_width = 224
img_height = 224


# Feature extractor
def get_features(model, df):
    features = []
    n_images = len(df)
    img_paths = list(df.local_image)
    for idx, img_path in enumerate(img_paths):
        print('getting features for %s %d/%d' %
              (img_path, idx+1, n_images))
        # Resize image to be 224x224
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        y = model.predict(x)
        # Vectorize the 7x7x512 tensor
        y = y.reshape(reduce(mul, y.shape, 1))
        features.append(y)
    return features


def load_model(config):
    if config['features']['model'] == 'vgg16':
        return VGG16(weights='imagenet', include_top=False)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args['config'])

    # Load VGG16, guys you better have a GPU...
    model = load_model(config)
    db = db_manager.get_db(config['general']['db_uri']
    df['features'] = get_features_cnn(model, df)

    pickle.dump(df, open(args.output_file, 'wb'))

if __name__ == "__main__":
    main(sys.argv[1:])
