from flask import request, make_response, jsonify, abort
from api.models import HostModel, HostSchema
import json
from flask import Blueprint

# ルーティング設定
host_update = Blueprint("host_update", __name__)


@host_update.route("", methods=["POST"])
def updateHost():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "host_id" in requested_data:
        abort(400, "host_id is a required!!")

    if not "host_name" in requested_data:
        abort(400, "host_name is a required!!")

    if not "host_password" in requested_data:
        abort(400, "host_password is a required!!")
    try:
        update_host = HostModel.updateHost(requested_data)
        host_schema = HostSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_host": host_schema.dump(update_host),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
