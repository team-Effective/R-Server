from flask import request, make_response, jsonify, abort
from api.models import HostModel, HostSchema
import json
from flask import Blueprint

# ルーティング設定
host_select = Blueprint("host_select", __name__)


@host_select.route("", methods=["POST"])
def selectHost():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "host_id" in requested_data:
        abort(400, "host_id is a required!!")

    try:
        select_host = HostModel.selectHost(requested_data.get("host_id"))
        host_schema = HostSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_host": host_schema.dump(select_host),
                }
            )
        )
    except AttributeError:
        return make_response(
            jsonify(
                {
                    "code": 500,
                    "Internal Server Error": "Data does not exist.",
                }
            )
        )
