from flask import request, make_response, jsonify, abort
from api.models import (
    MissionPlayerModel,
    MissionPlayerSchema,
    PlayerModel,
    PlayerSchema,
)
import json
from flask import Blueprint

# ルーティング設定
mission_player_select = Blueprint("mission_player_select", __name__)


@mission_player_select.route("/mission", methods=["POST"])
def selectPlayerListOfMission():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    # try:
    select_player_list_of_mission = MissionPlayerModel.selectPlayerListOfMission(
        requested_data.get("mission_id")
    )
    print(
        f"\n\n\nselect_player_list_of_missionを表示します\n{select_player_list_of_mission}\n"
    )

    select_mission_player_list = []
    for select_mission_player in select_player_list_of_mission:
        player_data = PlayerModel.selectPlayer(select_mission_player.player_id)
        if select_mission_player.mission_success is None:
            select_mission_player_list.append(
                {
                    "mission_id": select_mission_player.mission_id,
                    "player_id": select_mission_player.player_id,
                    "player_name": player_data.player_name,
                    "mission_success": None,
                }
            )
        else:
            select_mission_player_list.append(
                {
                    "mission_id": select_mission_player.mission_id,
                    "player_id": select_mission_player.player_id,
                    "player_name": player_data.player_name,
                    "mission_success": select_mission_player.mission_success,
                }
            )

    return make_response(
        jsonify(
            {
                "code": 200,
                "select_mission_player_list": select_mission_player_list,
            }
        )
    )

    # except AttributeError:
    #     return make_response(
    #         jsonify(
    #             {
    #                 "code": 500,
    #                 "Internal Server Error": "Data does not exist.",
    #             }
    #         )
    #     )


@mission_player_select.route("/once", methods=["POST"])
def selectMissionPlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    try:
        select_mission_player = MissionPlayerModel.selectMissionPlayer(requested_data)
        player_data = PlayerModel.selectPlayer(select_mission_player.player_id)
        if select_mission_player.mission_success is None:
            response_mission_player = {
                "mission_id": select_mission_player.mission_id,
                "player_id": select_mission_player.player_id,
                "player_name": player_data.player_name,
                "mission_success": None,
            }
        else:
            response_mission_player = {
                "mission_id": select_mission_player.mission_id,
                "player_id": select_mission_player.player_id,
                "player_name": player_data.player_name,
                "mission_success": select_mission_player.mission_success,
            }

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_mission_player": response_mission_player,
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
