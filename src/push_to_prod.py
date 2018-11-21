from db_manager import (get_db, PosterWeb, Poster, drop_posterweb)
from utils import create_folder
from PIL import Image as pil_image
from io import BytesIO
import base64


def copy_db_dev_prod(uri_db_dev, uri_db_prod):
    db_dev = get_db(uri_db_dev)
    db_prod = get_db(uri_db_prod)

    # PosterWeb.__table__.drop(db_prod)
    drop_posterweb(uri_db_prod)
    db_prod = get_db(uri_db_prod)

    data_dev = db_dev.query(Poster.id,
                            Poster.closest_posters,
                            Poster.title_display).all()
    data_prod = [PosterWeb(x.id,
                           x.closest_posters,
                           x.title_display)
                 for x in data_dev]

    db_prod.bulk_save_objects(data_prod)
    db_prod.commit()


def create_db_prod(uri_db_dev, uri_db_prod, path_img, path_thumb):
    copy_db_dev_prod(uri_db_dev, uri_db_prod)
    db_dev = get_db(uri_db_dev)
    create_folder(path_img)
    create_folder(path_thumb)

    data_posters = db_dev.query(Poster.id,
                                Poster.base64_img,
                                Poster.base64_thumb).all()
    for p in data_posters:
        img = pil_image.open(BytesIO(base64.b64decode(p.base64_img)))
        img.save('{}/{}.jpg'.format(path_img, p.id))
        img_thumb = pil_image.open(BytesIO(base64.b64decode(p.base64_thumb)))
        img_thumb.save('{}/{}.jpg'.format(path_thumb, p.id))
