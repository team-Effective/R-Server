from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.database import db, init_db
import config


def create_app():
    app = Flask(__name__)

    # CORS対応
    CORS(app)

    # DB設定を読み込む
    app.config.from_object(config.Config)
    with app.app_context():
        init_db(app)

    from .views.host_view.host_select import host_select
    from .views.host_view.host_insert import host_insert

    app.register_blueprint(host_select, url_prefix="/api/host/select")
    app.register_blueprint(host_insert, url_prefix="/api/host/insert")

    return app


app = create_app()
