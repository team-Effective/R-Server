from api.database import db, ma, metadata_obj
from flask import abort


class MissionModel(db.Model):
    __table__ = metadata_obj.tables["mission"]

    # ゲームの一件取得
    def selectMission(requested_mission_id):
        try:
            select_mission = (
                db.session.query(MissionModel)
                .filter(
                    MissionModel.__table__.columns.mission_id == requested_mission_id
                )
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if select_mission == None:
            return None
        else:
            return select_mission

    # ゲームの登録
    def insertMission(requested_mission):
        try:
            inserting_mission = MissionModel(
                mission_id=requested_mission.get("mission_id"),
                host_id=requested_mission.get("host_id"),
                mission_title=requested_mission.get("mission_title"),
            )
            db.session.add(inserting_mission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_mission


class MissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MissionModel
        fields = ("mission_id", "mission_title", "mission_detail")
