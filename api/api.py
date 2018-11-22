# -*- coding: utf-8 -*-

from src.db_manager import (get_db, Poster)
from src.utils import read_config
from flask_restful import Resource
from sqlalchemy.orm.attributes import InstrumentedAttribute
import os
import numpy as np


class ApiPosters(Resource):
    def __init__(self, path_config='./config/production.conf'):
        path_config = os.getenv('configapi')
        self.config = read_config(path_config)
        self.db = get_db(self.config['general']['db_uri'])

    def get_movie_by_id(self, id, fields):
        if isinstance(fields, InstrumentedAttribute):
            result = self.db.query(fields).filter_by(id=id).first()._asdict()
        else:
            result = self.db.query(*fields).filter_by(id=id).first()._asdict()
        return result

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
            data = [{'id': x[0], 'xy': list(x[1]), 'thumb': x[2]}
                    for x in my_query.all()]

            # n_data = my_query.count()
            # idx_rnd = np.random.choice(range(n_data), 2000, replace=False)
            # all_data = my_query.all()
            # rnd_data = [all_data[i] for i in idx_rnd]
            # data = [{'id': x[0], 'xy': list(x[1]), 'thumb': x[2]}
            #         for x in rnd_data]
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
