from api.database import db, ma
from flask import abort


class HostModel(db.Model):
    __tablename__ = "host"

    host_id = db.Column(db.varchar(32), primary_key=True)
    host_name = db.Column(db.varchar(16), nullable=False)
    host_password = db.Column(db.varchar(255), nullable=False)
    host_count = db.Column(db.int, nullable=False, default=0)
    now_host = db.Column(db.String(32), nullable=True)

    # 主催者の一件取得
    def getHost(requested_host_id):
        try:
            get_host = (
                db.session.query(HostModel)
                .filter(HostModel.__table__.columns.host_id == requested_host_id)
                .first()
            )
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        if get_host == None:
            return None
        else:
            return get_host

    # 主催者の登録
    def registHost(requested_host):
        try:
            registering_host = HostModel(
                host_id=requested_host.get("host_id"),
                host_name=requested_host.get("host_name"),
                host_password=requested_host.get("host_password"),
                host_count=requested_host.get("host_count"),
                now_host=requested_host.get("now_host"),
            )
            db.session.add(registering_host)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(400, e.args)
        return registering_host


class HostSchema(ma.ModelSchema):
    class Meta:
        model = HostModel
        fields = (
            "host_id",
            "host_name",
            "host_password",
            "host_count",
            "now_host",
        )
