#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
from functools import reduce
from operator import mul

import numpy as np
import tensorflow.keras.applications as applications
from keras.preprocessing import image
from tensorflow.keras import Sequential
from tensorflow.keras.layers import AveragePooling2D, Flatten
from tensorflow.keras.utils import load_img

import db_manager
import utils

img_width = 224
img_height = 224


models = {
    "ResNet50": {
        "model": applications.resnet50.ResNet50,
        "preprocess": applications.resnet50.preprocess_input,
    },
    "EfficientNetB0": {
        "model": applications.efficientnet.EfficientNetB0,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB1": {
        "model": applications.efficientnet.EfficientNetB1,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB2": {
        "model": applications.efficientnet.EfficientNetB2,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB3": {
        "model": applications.efficientnet.EfficientNetB3,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB4": {
        "model": applications.efficientnet.EfficientNetB4,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB5": {
        "model": applications.efficientnet.EfficientNetB5,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB6": {
        "model": applications.efficientnet.EfficientNetB6,
        "preprocess": applications.efficientnet.preprocess_input,
    },
    "EfficientNetB7": {
        "model": applications.efficientnet.EfficientNetB7,
        "preprocess": applications.efficientnet.preprocess_input,
    },
}

# Feature extractor
def batchify(data, preprocess_input, batch_size):
    for i in range(0, len(data), batch_size):
        x = [preprocess_input(np.array(load_img(d["path_img"], target_size=(img_width, img_height))))
             for d in data[i:i + batch_size]]
        yield np.array(x)


def get_features(data, model, preprocess_input, batchsize):
    features = []
    for i, batch in enumerate(batchify(data, preprocess_input, batchsize)):
        print(i)
        features.append(model(batch))
    return features

# def get_features(model, db):
#     """ Extract the last layer of a ConvNet and push it to a database.
#     The last layer (classification layer) is removed, and the output of the following
#     ConvNet now return a set of features. This technique is often referred as ``transfert learning''.

#     Parameters
#     ----------
#     model (keras.model): ConvNet with classification layer removed.
#     """
#     data = db.query(db_manager.Poster)
#     n_posters = data.count()
#     for i, poster in enumerate(data):
#         print('getting features for {} {}/{}'.format(
#             poster.path_img, i+1, n_posters))
#         # Resize image to be 224x224
#         img = load_img(poster.path_img,
#                        target_size=(img_width, img_height))
#         x = image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         x = preprocess_input(x)
#         y = model.predict(x)
#         # Vectorize the 7x7x512 tensor
#         poster.features = y.reshape(reduce(mul, y.shape, 1))
#     db.commit()
#     return data


def load_model(config):
    """ Load the weights of a pretrained ConvNet
    """
    model_str = config['features']['model']
    m = models[model_str]
    model = Sequential([
        m["model"](include_top=False, input_shape=(224, 224, 3)),
        AveragePooling2D(),
        Flatten(),
    ])
    return model, m["preprocess"]


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help="config file (default: config/development.conf",
                        default="./config/development.conf")
    args = parser.parse_args()
    config = utils.read_config(args.config)

    # Load VGG16 or ResNet50, guys you better have a GPU...
    import pickle
    data = pickle.load(open("yearly_urls.p", "rb"))
    model, preprocess_input = load_model(config)
    # db = db_manager.get_db(config['general']['db_uri'])
    data_features = get_features(data, model, preprocess_input, batchsize=32)
    pickle.dump(data_features, open("yearly_data_features.p", "wb"))
    # data_features = get_features(model, db)
    # db.commit()
    return data_features


if __name__ == "__main__":
    main(sys.argv[1:])
