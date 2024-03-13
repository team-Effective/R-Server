from api.database import db, ma, metadata_obj
from flask import abort
from sqlalchemy import and_


class GameMissionModel(db.Model):
    __table__ = metadata_obj.tables["game_mission"]

    # ゲームプレイヤーリストの取得
    def selectMissionListOfGame(requested_game_id):
        try:
            select_mission_list_of_game = (
                db.session.query(GameMissionModel)
                .filter(GameMissionModel.__table__.columns.game_id == requested_game_id)
                .all()
            )
        except Exception as e:
            abort(400, e.args)
        return select_mission_list_of_game

    # ゲームプレイヤーの一件取得
    def selectGameMission(requested_game_mission):
        try:
            select_game_mission = (
                db.session.query(GameMissionModel)
                .filter(
                    and_(
                        GameMissionModel.__table__.columns.game_id
                        == requested_game_mission.get("game_id"),
                        GameMissionModel.__table__.columns.mission_id
                        == requested_game_mission.get("mission_id"),
                    )
                )
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if select_game_mission == None:
            return None
        else:
            return select_game_mission

    # ゲームプレイヤーの登録
    def insertGameMission(requested_game_Mission):
        try:
            inserting_game_Mission = GameMissionModel(
                game_id=requested_game_Mission.get("game_id"),
                mission_id=requested_game_Mission.get("mission_id"),
            )
            db.session.add(inserting_game_Mission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_game_Mission

    # ゲームプレイヤーの更新
    def updateGameMission(requested_game_mission):
        try:
            updating_game_mission = (
                db.session.query(GameMissionModel)
                .filter(
                    and_(
                        GameMissionModel.__table__.columns.game_id
                        == requested_game_mission.get("game_id"),
                        GameMissionModel.__table__.columns.mission_id
                        == requested_game_mission.get("mission_id"),
                    )
                )
                .first()
            )
            if requested_game_mission.get("mission_finish") is not None:
                updating_game_mission.mission_finish = requested_game_mission.get(
                    "mission_finish"
                )
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        db.session.add(updating_game_mission)
        db.session.commit()
        return updating_game_mission


class GameMissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GameMissionModel
        fields = ("game_id", "mission_id", "mission_finish")
