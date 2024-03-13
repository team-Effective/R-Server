from api.database import db, ma, metadata_obj
from api.models import HostModel, HostSchema
from flask import abort


class HostPlayerModel(db.Model):
    __table__ = metadata_obj.tables["host_player"]

    # プレイヤーの主催者単位取得
    def selectPlayerListOfHost(requested_host_id):
        try:
            select_player_list_of_host = (
                db.session.query(HostPlayerModel)
                .filter(HostPlayerModel.__table__.columns.host_id == requested_host_id)
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return select_player_list_of_host

    # 主催者ごとのプレイヤーの登録
    def insertHostPlayer(requested_host):
        try:
            inserting_host_player = HostPlayerModel(
                host_id=requested_host.get("host_id"),
                player_id=requested_host.get("player_id"),
            )
            db.session.add(inserting_host_player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_host_player


class HostPlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HostPlayerModel
        fields = (
            "host_id",
            "player_id",
        )
