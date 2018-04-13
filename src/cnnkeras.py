import numpy as np
from os import listdir
from os.path import isfile, join
import h5py
from PIL import Image

from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers import Convolution2D, ZeroPadding2D, MaxPooling2D
from keras.optimizers import SGD

from keras import backend as K
K.set_image_dim_ordering('th')

def get_image(path, w, h):
    img = Image.open(path)
    if img.mode == 'L' or img.mode == 'RGBA':
        img = img.convert('RGB')
    img = img.resize((w, h), Image.ANTIALIAS)
    im2 = np.array(img.getdata(), np.uint8)
    im3 = np.array(img.getdata(), np.uint8)
    im2[:,0] = im3[:,2]
    im2[:,2] = im3[:,0]
    im2 = im2.reshape(img.size[1], img.size[0], 3).astype(np.float32)
    im2[:,:,0] -= 103.939
    im2[:,:,1] -= 116.779
    im2[:,:,2] -= 123.68
    im2 = im2.transpose((2,0,1))
    im2 = np.expand_dims(im2, axis=0)
    return im2

# Source: https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3
def VGG_16():
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(3,224,224)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(64, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(128, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2) ,strides=(2,2)))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(256, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2) , strides=(2,2)))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2),strides=(2,2)))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Convolution2D(512, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2),strides=(2,2)))
    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))

    # Remove last layer specific to classification purpose
    # The last Dense layers followed by a relu will be use as features 

    #model.add(Dropout(0.5))
    #model.add(Dense(1000, activation='softmax'))
    #if weights_path:
    #   model.load_weights(weights_path)
    return model


def load_weights(model, weights_path):
    f = h5py.File(weights_path)
    for k in range(f.attrs['nb_layers']):
        print(k)
        if k >= len(model.layers):
            break
        g = f['layer_{}'.format(k)]
        layer = model.layers[k]
        weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
        if layer.__class__.__name__ in ['Convolution1D', 
                                        'Convolution2D', 
                                        'Convolution3D', 
                                        'AtrousConvolution2D',
                                        'Conv2D']:
            weights[0] = np.transpose(weights[0], (2, 3, 1, 0))
        model.layers[k].set_weights(weights)
