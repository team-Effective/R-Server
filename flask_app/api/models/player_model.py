from api.database import db, ma
from flask import abort


class PlayerModel(db.Model):
    __tablename__ = "player"

    player_id = db.Column(db.varchar(32), primary_key=True)
    player_name = db.Column(db.varchar(16), nullable=False)
    player_password = db.Column(db.varchar(255), nullable=False)
    match_count = db.Column(db.int, nullable=False, default=0)
    alive_count = db.Column(db.int, nullable=False, default=0)
    now_game = db.Column(db.String(32), nullable=True)

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
                match_count=requested_player.get("match_count"),
                alive_count=requested_player.get("alive_count"),
                now_game=requested_player.get("now_game"),
            )
            db.session.add(registering_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return registering_player


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = PlayerModel
        fields = (
            "player_id",
            "player_name",
            "player_password",
            "match_count",
            "alive_count",
            "now_game",
        )
