from api.database import db, ma, metadata_obj
from flask import abort
from sqlalchemy import and_


class GamePlayerModel(db.Model):
    __table__ = metadata_obj.tables["game_player"]

    # ゲームプレイヤーリストの取得
    def selectPlayerListOfGame(requested_game_id):
        try:
            select_player_list_of_game = (
                db.session.query(GamePlayerModel)
                .filter(GamePlayerModel.__table__.columns.game_id == requested_game_id)
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return select_player_list_of_game

    # ゲームプレイヤーの一件取得
    def selectGamePlayerOnce(requested_game_player):
        try:
            select_game_player = (
                db.session.query(GamePlayerModel)
                .filter(
                    and_(
                        GamePlayerModel.__table__.columns.game_id
                        == requested_game_player.get("game_id"),
                        GamePlayerModel.__table__.columns.player_id
                        == requested_game_player.get("player_id"),
                    )
                )
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if select_game_player == None:
            return None
        else:
            return select_game_player

    # ゲームプレイヤーの登録
    def insertGamePlayer(requested_game_Player):
        try:
            inserting_game_Player = GamePlayerModel(
                game_id=requested_game_Player.get("game_id"),
                player_id=requested_game_Player.get("player_id"),
            )
            db.session.add(inserting_game_Player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_game_Player

    # ゲームプレイヤーの更新
    def updateGamePlayer(requested_game_player):
        try:
            updating_game_player = (
                db.session.query(GamePlayerModel)
                .filter(
                    and_(
                        GamePlayerModel.__table__.columns.game_id
                        == requested_game_player.get("game_id"),
                        GamePlayerModel.__table__.columns.player_id
                        == requested_game_player.get("player_id"),
                    )
                )
                .first()
            )
            if requested_game_player.get("now_alive") is not None:
                updating_game_player.now_alive = requested_game_player.get("now_alive")
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        db.session.add(updating_game_player)
        db.session.commit()
        return updating_game_player


class GamePlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GamePlayerModel
        fields = ("game_id", "player_id", "now_alive")
