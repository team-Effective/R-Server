from api.database import db, ma, metadata_obj
from flask import abort


class GameModel(db.Model):
    __table__ = metadata_obj.tables["game"]

    # ゲームの主催者単位取得
    def selectGameListOfHost(requested_host_id):
        try:
            select_game_list_of_host = (
                db.session.query(GameModel)
                .filter(GameModel.__table__.columns.host_id == requested_host_id)
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return select_game_list_of_host

    # ゲームの一件取得
    def selectGame(requested_game_id):
        try:
            select_game = (
                db.session.query(GameModel)
                .filter(GameModel.__table__.columns.game_id == requested_game_id)
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if select_game == None:
            return None
        else:
            return select_game

    # ゲームの登録
    def insertGame(requested_game):
        try:
            inserting_game = GameModel(
                game_id=requested_game.get("game_id"),
                host_id=requested_game.get("host_id"),
                game_title=requested_game.get("game_title"),
            )
            db.session.add(inserting_game)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_game


class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GameModel
        fields = ("game_id", "host_id", "game_title")
