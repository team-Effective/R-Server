from api.database import db, ma
from flask import abort


class GameModel(db.Model):
    __tablename__ = "game"

    game_id = db.Column(db.varchar(32), primary_key=True)
    host_id = db.Column(db.varchar(32), db.ForeignKey("host.host_id"))
    game_title = db.Column(db.String(32), nullable=False)

    # ゲームの主催者単位取得
    def getGameListOfHost(requested_host_id):
        try:
            get_game_list_of_host = (
                db.session.query(GameModel)
                .filter(GameModel.__table__.columns.host_id == requested_host_id)
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return get_game_list_of_host

    # ゲームの一件取得
    def getGame(requested_game_id):
        try:
            get_game = (
                db.session.query(GameModel)
                .filter(GameModel.__table__.columns.game_id == requested_game_id)
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if get_game == None:
            return None
        else:
            return get_game

    # ゲームの登録
    def registGame(requested_game):
        try:
            registering_game = GameModel(
                game_id=requested_game.get("game_id"),
                host_id=requested_game.get("host_id"),
                game_title=requested_game.get("game_title"),
            )
            db.session.add(registering_game)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return registering_game


class GameSchema(ma.ModelSchema):
    class Meta:
        model = GameModel
        fields = (
            "game_id",
            "host_id",
            "game_title",
        )
