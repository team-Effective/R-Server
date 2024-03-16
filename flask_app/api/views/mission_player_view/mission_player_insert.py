from flask import request, make_response, jsonify, abort
from api.models import MissionPlayerModel, MissionPlayerSchema
import json
from flask import Blueprint

# ルーティング設定
mission_player_insert = Blueprint("mission_player_insert", __name__)


@mission_player_insert.route("", methods=["POST"])
def insertMissionPlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    try:
        insert_mission_player = MissionPlayerModel.insertMissionPlayer(requested_data)
        mission_player_schema = MissionPlayerSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "insert_mission_player": mission_player_schema.dump(
                        insert_mission_player
                    ),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
