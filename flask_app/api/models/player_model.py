from api.database import db, ma, metadata_obj
from flask import abort


class PlayerModel(db.Model):
    __table__ = "player"

    # プレイヤーの一件取得
    def selectPlayer(requested_player_id):
        try:
            get_player = (
                db.session.query(PlayerModel)
                .filter(PlayerModel.__table__.columns.player_id == requested_player_id)
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if get_player == None:
            return None
        else:
            return get_player

    # プレイヤーの登録
    def insertPlayer(requested_player):
        try:
            inserting_player = PlayerModel(
                player_id=requested_player.get("player_id"),
                player_name=requested_player.get("player_name"),
            )
            db.session.add(inserting_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_player

    # プレイヤーの更新
    def updateHost(requested_player):
        try:
            updating_player = (
                db.session.query(PlayerModel)
                .filter(
                    PlayerModel.__table__.columns.player_id
                    == requested_player.get("player_id")
                )
                .first()
            )
            if requested_player.get("player_name") is not None:
                updating_player.player_name = requested_player.get("player_name")
            if requested_player.get("match_count") is not None:
                updating_player.match_count = requested_player.get("match_count")
            if requested_player.get("alive_count") is not None:
                updating_player.alive_count = requested_player.get("alive_count")
            updating_player.now_game = requested_player.get("now_game")
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        db.session.add(updating_player)
        db.session.commit()
        return updating_player


class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlayerModel
