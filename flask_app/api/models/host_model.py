from api.database import db, ma, metadata_obj
from flask import abort


class HostModel(db.Model):
    __table__ = metadata_obj.tables["host"]

    # 主催者の一件取得
    def selectHost(requested_host_id):
        try:
            select_host = (
                db.session.query(HostModel)
                .filter(HostModel.__table__.columns.host_id == requested_host_id)
                .first()
            )
        except Exception as e:
            abort(400, e.args)
        if select_host == None:
            return None
        else:
            return select_host

    # 主催者の登録
    def insertHost(requested_host):
        try:
            inserting_host = HostModel(
                host_id=requested_host.get("host_id"),
                host_name=requested_host.get("host_name"),
                host_password=requested_host.get("host_password"),
            )
            db.session.add(inserting_host)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return inserting_host

    # 主催者の更新
    def updateHost(requested_host):
        try:
            updating_host = (
                db.session.query(HostModel)
                .filter(
                    HostModel.__table__.columns.host_id == requested_host.get("host_id")
                )
                .first()
            )
            if requested_host.get("host_name") is not None:
                updating_host.host_name = requested_host.get("host_name")
            if requested_host.get("host_password") is not None:
                updating_host.host_password = requested_host.get("host_password")
            if requested_host.get("host_count") is not None:
                updating_host.host_count = requested_host.get("host_count")
            updating_host.now_host = requested_host.get("now_host")
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        db.session.add(updating_host)
        db.session.commit()
        return updating_host


class HostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HostModel
        fields = ("host_id", "host_name", "host_password", "host_count", "now_host")
