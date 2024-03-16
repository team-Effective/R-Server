from api.database import db, ma, metadata_obj
from flask import abort
from sqlalchemy import and_


class MissionPlayerModel(db.Model):
    __table__ = metadata_obj.tables["mission_player"]

    # ミッションプレイヤーリストの取得
    def selectPlayerListOfMission(requested_mission_id):
        try:
            select_player_list_of_mission = (
                db.session.query(MissionPlayerModel)
                .filter(
                    MissionPlayerModel.__table__.columns.mission_id
                    == requested_mission_id
                )
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return select_player_list_of_mission

    # ミッションプレイヤーの一件取得
    def selectMissionPlayerOnce(requested_mission_player):
        try:
            select_mission_player = (
                db.session.query(MissionPlayerModel)
                .filter(
                    and_(
                        MissionPlayerModel.__table__.columns.mission_id
                        == requested_mission_player.get("mission_id"),
                        MissionPlayerModel.__table__.columns.player_id
                        == requested_mission_player.get("player_id"),
                    )
                )
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if select_mission_player == None:
            return None
        else:
            return select_mission_player

    # ミッションプレイヤーの登録
    def insertMissionPlayer(requested_mission_Player):
        try:
            inserting_mission_Player = MissionPlayerModel(
                mission_id=requested_mission_Player.get("mission_id"),
                player_id=requested_mission_Player.get("player_id"),
            )
            db.session.add(inserting_mission_Player)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_mission_Player

    # ミッションプレイヤーの更新
    def updateMissionPlayer(requested_mission_player):
        try:
            updating_mission_player = (
                db.session.query(MissionPlayerModel)
                .filter(
                    and_(
                        MissionPlayerModel.__table__.columns.mission_id
                        == requested_mission_player.get("mission_id"),
                        MissionPlayerModel.__table__.columns.player_id
                        == requested_mission_player.get("player_id"),
                    )
                )
                .first()
            )

            if requested_mission_player.get("mission_success") is not None:
                updating_mission_player.mission_success = requested_mission_player.get(
                    "mission_success"
                )

        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        db.session.add(updating_mission_player)
        db.session.commit()
        return updating_mission_player


class MissionPlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MissionPlayerModel
        fields = ("mission_id", "player_id", "mission_success")
