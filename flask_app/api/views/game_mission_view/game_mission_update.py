from flask import request, make_response, jsonify, abort
from api.models import GameMissionModel, GameMissionSchema
import json
from flask import Blueprint

# ルーティング設定
game_mission_update = Blueprint("game_mission_update", __name__)


@game_mission_update.route("/finish", methods=["POST"])
def updateGameMissionFinish():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    if not "game_id" in requested_data:
        abort(400, "game_id is a required!!")

    try:
        update_mission = {
            "game_id": requested_data.get("game_id"),
            "mission_id": requested_data.get("mission_id"),
            "mission_finish": True,
        }
        update_game_mission_finish = GameMissionModel.updateGameMission(update_mission)
        mission_schema = GameMissionSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_game_mission_finish": mission_schema.dump(
                        update_game_mission_finish
                    ),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
