#!/bin/sh

python get_posters.py --range 1920-2016 -o ./cnn_posters_1920-2016.p
python get_features_from_cnn.py --input_file ./cnn_posters_1920-2016.p -o ./cnn_posters_1920-2016_feat.p -v ./vgg16_weights.h5
python get_posters.py --input_file ./cnn_posters_1920-2016_feat.p --input_file ./cnn_posters_1920-2016_feat.p -n_sample 3000 --output_file datasets/x.json
