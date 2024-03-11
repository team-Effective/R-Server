from api.database import db, ma, metadata_obj
from flask import abort
from sqlalchemy import and_


class GamePlayerModel(db.Model):
    __table__ = "game_player"

    # ゲームプレイヤーリストの取得
    def getGamePlayerList(requested_game_id):
        try:
            get_game_player_list = (
                db.session.query(GamePlayerModel)
                .filter(GamePlayerModel.__table__.columns.game_id == requested_game_id)
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return get_game_player_list

    # ゲームプレイヤーの一件取得
    def getGame(requested_game_id, requested_player_id):
        try:
            get_game_player = (
                db.session.query(GamePlayerModel)
                .filter(
                    and_(
                        GamePlayerModel.__table__.columns.game_id == requested_game_id,
                        GamePlayerModel.__table__.columns.player_id
                        == requested_player_id,
                    )
                )
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if get_game_player == None:
            return None
        else:
            return get_game_player

    # ゲームプレイヤーの登録
    def registGamePlayer(requested_game_Player):
        try:
            registering_game_Player = GamePlayerModel(
                game_id=requested_game_Player.get("game_id"),
                player_id=requested_game_Player.get("player_id"),
            )
            db.session.add(requested_game_Player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return registering_game_Player


class GamePlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GamePlayerModel