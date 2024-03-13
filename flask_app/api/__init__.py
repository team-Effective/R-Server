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
    from .views.host_view.host_update import host_update

    app.register_blueprint(host_select, url_prefix="/api/host/select")
    app.register_blueprint(host_insert, url_prefix="/api/host/insert")
    app.register_blueprint(host_update, url_prefix="/api/host/update")

    from .views.player_view.player_select import player_select
    from .views.player_view.player_insert import player_insert
    from .views.player_view.player_update import player_update

    app.register_blueprint(player_select, url_prefix="/api/player/select")
    app.register_blueprint(player_insert, url_prefix="/api/player/insert")
    app.register_blueprint(player_update, url_prefix="/api/player/update")

    from .views.host_player_view.host_player_select import host_player_select
    from .views.host_player_view.host_player_insert import host_player_insert

    app.register_blueprint(host_player_select, url_prefix="/api/host_player/select")
    app.register_blueprint(host_player_insert, url_prefix="/api/host_player/insert")

    from .views.game_view.game_select import game_select
    from .views.game_view.game_insert import game_insert

    app.register_blueprint(game_select, url_prefix="/api/game/select")
    app.register_blueprint(game_insert, url_prefix="/api/game/insert")

    from .views.game_player_view.game_player_select import game_player_select
    from .views.game_player_view.game_player_insert import game_player_insert

    app.register_blueprint(game_player_select, url_prefix="/api/game_player/select")
    app.register_blueprint(game_player_insert, url_prefix="/api/game_player/insert")

    return app


app = create_app()
