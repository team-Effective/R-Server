from flask import request, make_response, jsonify, abort
from api.models import GameMissionModel, GameMissionSchema
import json
from flask import Blueprint

# ルーティング設定
game_mission_insert = Blueprint("game_mission_insert", __name__)


@game_mission_insert.route("", methods=["POST"])
def insertGameMission():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "game_id" in requested_data:
        abort(400, "game_id is a required!!")

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    try:
        insert_game_mission = GameMissionModel.insertGameMission(requested_data)
        game_mission_schema = GameMissionSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "insert_game_mission": game_mission_schema.dump(
                        insert_game_mission
                    ),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
