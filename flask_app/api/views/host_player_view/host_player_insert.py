from flask import request, make_response, jsonify, abort
from api.models import HostPlayerModel, HostPlayerSchema
import json
from flask import Blueprint

# ルーティング設定
host_player_insert = Blueprint("host_player_insert", __name__)


@host_player_insert.route("", methods=["POST"])
def insertHostPlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "host_id" in requested_data:
        abort(400, "host_id is a required!!")

    try:
        insert_host_player = HostPlayerModel.insertHostPlayer(requested_data)
        host_player_schema = HostPlayerSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "insert_player": host_player_schema.dump(insert_host_player),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
