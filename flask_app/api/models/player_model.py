from api.database import db, ma, metadata_obj
from flask import abort


class PlayerModel(db.Model):
    __table__ = "player"

    # プレイヤーの全件取得
    def getPlayerList():
        try:
            get_player_list = db.session.query(PlayerModel).all()
        except Exception as e:
            abort(400, e.args)
        if get_player_list == None:
            return []
        else:
            return get_player_list

    # プレイヤーの一件取得
    def getPlayer(requested_player_id):
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
    def registPlayer(requested_player):
        try:
            registering_player = PlayerModel(
                player_id=requested_player.get("player_id"),
                player_name=requested_player.get("player_name"),
                player_password=requested_player.get("player_password"),
            )
            db.session.add(registering_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return registering_player


class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlayerModel
