# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, make_response
from flask_restful import Api, Resource
from src.db_manager import (get_db, Poster)
from flask_cors import CORS
from src.utils import read_config
from sqlalchemy.orm.attributes import InstrumentedAttribute
import os
from flask_cache import Cache
import numpy as np
from flask import request
import urllib


appli = Flask(__name__)
CORS(appli)
cache = Cache(appli, config={'CACHE_TYPE': 'redis',
                             'CACHE_REDIS_HOST': '127.0.0.1',
                             'CACHE_REDIS_PORT': 6379})

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def cache_key():
    args = request.args
    key = request.path + '?' + urllib.urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    return key

class ApiPosters(Resource):
    def __init__(self, path_config='./config/production.conf'):
        path_config = os.getenv('configapi')
        self.config = read_config(path_config)
        self.db = get_db(self.config['general']['db_uri'])

    @cache.memoize(50)
    def get_movie_by_id(self, id, fields):
        if isinstance(fields, InstrumentedAttribute):
            result = self.db.query(fields).filter_by(id=id).first()._asdict()
        else:
            result = self.db.query(*fields).filter_by(id=id).first()._asdict()
        return result

    @cache.cached(timeout=60, key_prefix=cache_key)
    def get(self, id):
        """ Retrieve the movie poster with specific id along with
        its closest movie posters
        """

        if id == 'idmovies':
            data = {x[1]: x[0] for
                    x in self.db.query(Poster.id,
                                       Poster.title_display).all()}
        elif id == '2d':
            fields = (Poster.id,
                      Poster.features_pca,
                      Poster.path_thumb)
            my_query = self.db.query(*fields).filter(~Poster.path_img.contains('ver'))
            # data = [{'id': x[0], 'xy': list(x[1]), 'thumb': x[2]}
            #         for x in my_query.all()]

            n_data = my_query.count()
            idx_rnd = np.random.choice(range(n_data), 2000, replace=False)
            all_data = my_query.all()
            rnd_data = [all_data[i] for i in idx_rnd]
            data = [{'id': x[0], 'xy': list(x[1]), 'thumb': x[2]}
                    for x in rnd_data]
        else:
            id = int(id)
            print('movie id: {}'.format(id))
            fields = (Poster.closest_posters)
            ids_closest = self.get_movie_by_id(id, fields)

            ids = [id]
            ids += [int(x) for x in ids_closest['closest_posters'].split(',')]
            fields = (Poster.id,
                      Poster.title_display,
                      Poster.path_img)

            data = [self.get_movie_by_id(x, fields) for x in ids]
        return data


class index(Resource):
    """ print documentation """
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)


class index_complete(Resource):
    """ print documentation """
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index_complete.html'),
                             200, headers)


routes = ['/', '/index.html']
api.add_resource(index, *routes)
api.add_resource(index_complete, '/index_complete.html')
api.add_resource(ApiPosters, '/v1/<id>')
appli.register_blueprint(api_bp)


if __name__ == "__main__":
    appli.run(host="0.0.0.0", debug=True)
