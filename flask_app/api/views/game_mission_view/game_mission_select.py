from flask import request, make_response, jsonify, abort
from api.models import GameMissionModel, GameMissionSchema, MissionModel, MissionSchema
import json
from flask import Blueprint

# ルーティング設定
game_mission_select = Blueprint("game_mission_select", __name__)


@game_mission_select.route("/game", methods=["POST"])
def selectMissionListOfGame():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    try:
        select_mission_list_of_game = GameMissionModel.selectMissionListOfGame(
            requested_data.get("game_id")
        )
        select_game_mission_list = []
        for select_game_mission in select_mission_list_of_game:
            mission_data = MissionModel.selectMission(select_game_mission.mission_id)
            select_game_mission_list.append(
                {
                    "game_id": select_game_mission.game_id,
                    "mission_id": select_game_mission.mission_id,
                    "mission_title": mission_data.mission_title,
                    "mission_finish": select_game_mission.mission_finish,
                }
            )

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_game_mission_list": select_game_mission_list,
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


@game_mission_select.route("/once", methods=["POST"])
def selectGameMission():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    try:
        select_game_mission = GameMissionModel.selectGameMission(requested_data)
        mission_data = MissionModel.selectMission(select_game_mission.mission_id)
        response_game_mission = {
            "game_id": select_game_mission.game_id,
            "mission_id": select_game_mission.mission_id,
            "mission_title": mission_data.mission_title,
            "mission_finish": select_game_mission.mission_finish,
        }

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_game_mission": response_game_mission,
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
