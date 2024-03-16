from flask import request, make_response, jsonify, abort
from api.models import MissionPlayerModel, MissionPlayerSchema
import json
from flask import Blueprint

# ルーティング設定
mission_player_update = Blueprint("mission_player_update", __name__)


@mission_player_update.route("/success", methods=["POST"])
def updateMissionSuccess():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    try:
        update_player = {
            "mission_id": requested_data.get("mission_id"),
            "player_id": requested_data.get("player_id"),
            "mission_success": True,
        }
        update_mission_player_success = MissionPlayerModel.updateMissionPlayer(
            update_player
        )
        player_schema = MissionPlayerSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_mission_player_success": player_schema.dump(
                        update_mission_player_success
                    ),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)


@mission_player_update.route("/failed", methods=["POST"])
def updateMissionFailed():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    try:
        update_player = {
            "mission_id": requested_data.get("mission_id"),
            "player_id": requested_data.get("player_id"),
            "mission_success": False,
        }
        update_mission_player_failed = MissionPlayerModel.updateMissionPlayer(
            update_player
        )
        player_schema = MissionPlayerSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_mission_player_failed": player_schema.dump(
                        update_mission_player_failed
                    ),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
