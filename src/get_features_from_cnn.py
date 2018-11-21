#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from functools import reduce
from operator import mul

import numpy as np

import db_manager
import utils
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.resnet50 import ResNet50
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image

img_width = 224
img_height = 224


# Feature extractor
def get_features(model, db):
    """ Extract the last layer of a ConvNet and push it to a database.
    The last layer (classification layer) is removed, and the output of the following
    ConvNet now return a set of features. This technique is often referred as ``transfert learning''.

    Parameters
    ----------
    model (keras.model): ConvNet with classification layer removed.
    """
    data = db.query(db_manager.Poster)
    n_posters = data.count()
    for i, poster in enumerate(data):
        print('getting features for {} {}/{}'.format(
            poster.path_img, i+1, n_posters))
        # Resize image to be 224x224
        img = image.load_img(poster.path_img,
                             target_size=(img_width, img_height))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        y = model.predict(x)
        # Vectorize the 7x7x512 tensor
        poster.features = y.reshape(reduce(mul, y.shape, 1))
    db.commit()
    return data


def load_model(config):
    """ Load the weights of a pretrained ConvNet
    """
    if config['features']['model'] == 'vgg16':
        return VGG16(weights='imagenet', include_top=False)

    if config['features']['model'] == 'resnet50':
        return ResNet50(weights='imagenet', include_top=False)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)

    # Load VGG16, guys you better have a GPU...
    model = load_model(config)
    db = db_manager.get_db(config['general']['db_uri'])

    data_features = get_features(model, db)
    db.commit()
    return data_features


if __name__ == "__main__":
    main(sys.argv[1:])
