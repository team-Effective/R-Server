from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData


db = SQLAlchemy()
ma = Marshmallow()
metadata_obj = MetaData()


# アプリでDB操作を行えるように初期設定する
def init_db(app):
    db.init_app(app)
    metadata_obj.reflect(bind=db.engine)
