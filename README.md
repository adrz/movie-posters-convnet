[![Build
Status](https://travis-ci.org/adrz/movie-posters-convnet.svg?branch=master)](https://travis-ci.org/adrz/movie-posters-convnet)
[![codecov](https://codecov.io/gh/adrz/movie-posters-convnet/branch/master/graph/badge.svg)](https://codecov.io/gh/adrz/movie-posters-convnet)

# Overview

Unsupervised clustering of movie posters with features extracted from Convolutional Neural Network. Visualization using d3js.

This project is divided into 3 main scripts:
* get_posters.py
  * retrieve the posters from impawards.com.
  * create a thumbnail for each posters for the visualization.
* get_features_from_cnn.py
  * extract the last full-connected layer of size 4096 of VGG-16 [paper](https://arxiv.org/abs/1409.1556)
* get_data_visu.py
  * dimension reduction for data-visualization
  * first PCA reduction then t-SNE to convert the 4096 dimensions features into a 2 dimensions features
  * t-SNE: [paper](http://jmlr.org/papers/volume9/vandermaaten08a/vandermaaten08a.pdf)
  * t-SNE: [tutorial on t-SNE](http://distill.pub/2016/misread-tsne/)

To get parameters descriptions:
* python get_XXX.py --help

# Setup

## Requirements

### OS
* Linux/Unix/OSX (requirement for wget)
* Python 3.3+
* ImageMagick

### Packages Python
* BeautifulSoup 4.4
* [Tensorflow 1.0](https://www.tensorflow.org/install/)
* Keras
* Pandas
* pickle
* urllib
* sklearn
* numpy
* h5py
* PIL
* [Multicore-TSNE](https://github.com/DmitryUlyanov/Multicore-TSNE)

## Installation

Download the VGG-16 weights: [vgg16_weights.h5](https://drive.google.com/file/d/0Bz7KyqmuGsilT0J5dmRCM0ROVHc/view?usp=sharing)

```sh
$ git clone https://github.com/aDrz/movie-posters-convnet.git
```

# Usage

## Computation
After cloning you can just launch the bash script that will:
* download posters from 1920 to 2016
* compute features
* perform dimensional reduction on features of 3000 randomly choosen posters

```sh
$ chmox +x run-posters-cnn.sh
$ ./run-posters-cnn.sh
```

Then grab a coffee...

## Visualization
First install a HTTP server (webfsd):
```sh
$ sudo apt-get install webfsd
```

Then launch index.html into your favorite browser:
```sh
$ chromium 127.0.0.1:8000/index.html?data.json
```


## Results
Cherry-piking from the top-200 closest couple of posters (relative to cosine distance):

<div align = 'center'>
<a href = 'examples/thumb-1030-000.jpg'><img src = 'examples/thumb-300-000.png', hspace="20"></a>
<a href = 'examples/thumb-1030-001.jpg'><img src = 'examples/thumb-300-001.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-002.jpg'><img src = 'examples/thumb-300-002.png', hspace="20"></a>
<a href = 'examples/thumb-1030-003.jpg'><img src = 'examples/thumb-300-003.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-004.jpg'><img src = 'examples/thumb-300-004.png', hspace="20"></a>
<a href = 'examples/thumb-1030-005.jpg'><img src = 'examples/thumb-300-005.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-006.jpg'><img src = 'examples/thumb-300-006.png', hspace="20"></a>
<a href = 'examples/thumb-1030-007.jpg'><img src = 'examples/thumb-300-007.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-008.jpg'><img src = 'examples/thumb-300-008.png', hspace="20"></a>
<a href = 'examples/thumb-1030-009.jpg'><img src = 'examples/thumb-300-009.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-010.jpg'><img src = 'examples/thumb-300-010.png', hspace="20"></a>
<a href = 'examples/thumb-1030-011.jpg'><img src = 'examples/thumb-300-011.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-012.jpg'><img src = 'examples/thumb-300-012.png', hspace="20"></a>
<a href = 'examples/thumb-1030-013.jpg'><img src = 'examples/thumb-300-013.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-014.jpg'><img src = 'examples/thumb-300-014.png', hspace="20"></a>
<a href = 'examples/thumb-1030-015.jpg'><img src = 'examples/thumb-300-015.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-016.jpg'><img src = 'examples/thumb-300-016.png', hspace="20"></a>
<a href = 'examples/thumb-1030-017.jpg'><img src = 'examples/thumb-300-017.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-018.jpg'><img src = 'examples/thumb-300-018.png', hspace="20"></a>
<a href = 'examples/thumb-1030-019.jpg'><img src = 'examples/thumb-300-019.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-020.jpg'><img src = 'examples/thumb-300-020.png', hspace="20"></a>
<a href = 'examples/thumb-1030-021.jpg'><img src = 'examples/thumb-300-021.png', hspace="20"></a>
<br><br><br>
<a href = 'examples/thumb-1030-022.jpg'><img src = 'examples/thumb-300-022.png', hspace="20"></a>
<a href = 'examples/thumb-1030-023.jpg'><img src = 'examples/thumb-300-023.png', hspace="20"></a>
</div>


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* d3js plot: from [https://github.com/douglasbagnall/image-tsne](https://github.com/douglasbagnall/image-tsne)
* [VGG-16 pre-trained model for Keras](https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3)
* posters: [IMP Awards](http://impawards.com)



<!-- ## Postgresql -->
<!-- sudo -u postgres createuser movieposters -->
<!-- sudo -u postgres createdb movieposters -->
<!-- sudo -u postgres psql -->
<!-- alter user movieposters with encrypted password 'm'; -->
<!-- grant all privileges on database movieposters to movieposters ; -->


## Server install
ssh root@51.15.248.42
# ssh adrien@35.196.172.250

sudo apt update
sudo apt upgrade -y
sudo apt install -y git python-requests software-properties-common \
python-software-properties \
apt-transport-https \
python-pip \
python3-dev \
python-virtualenv \
libpcre3 libpcre3-dev \
nginx
	
mkdir /app && cd /app

### Download database
wget https://gist.githubusercontent.com/adrz/2484cccdc5624a2d36c4d3a46499a72a/raw/7b13cd932c3425525e064dd19ede221c3725d242/google_drive.py
python google_drive.py 1k2sy5Ncjr2L6LgM12Nc_W0Ht_WjiFa2q ./data.tar.gz
tar -xzf data.tar.gz

### Install docker+docker-compose
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce
sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


git clone https://github.com/adrz/movie-posters-convnet
git clone -b development https://github.com/adrz/movie-posters-convnet


export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo dpkg-reconfigure -f noninteractive locales


mv data/ movie-posters-convnet/
cd movie-posters-convnet
mkdir static && ln -s $(pwd)/data $(pwd)/static/
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary
pip install uwsgi
sudo docker run --name some-postgres --restart unless-stopped -e POSTGRES_PASSWORD=m -d -p 5432:5432 postgres

sudo apt install -y postgresql-client
PGPASSWORD=m psql -h 0.0.0.0 -U postgres -c 'create database movieposters;'
PGPASSWORD=m psql -h 0.0.0.0 -U postgres movieposters < data/moviesweb.db


## 

### nginx / web


### In file /etc/systemd/system/movieposters.service

sudo cp movieposters.service /etc/systemd/system/movieposters.service

sudo service movieposters start
sudo systemctl enable movieposters

## in file /etc/nginx/sites-available/movieposters

sudo cp flask-site-nginx.conf /etc/nginx/sites-available/movieposters

sudo rm -rf /etc/nginx/sites-available/default
sudo rm -rf /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/movieposters /etc/nginx/sites-enabled/movieposters

sudo service nginx restart
### Bootstrap:
scw exec ifconfig eth0 | grep "inet addr" | cut -d ':' -f 2 | cut -d ' ' -f 1





