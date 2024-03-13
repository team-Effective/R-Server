from flask import request, make_response, jsonify, abort
from api.models import HostPlayerModel, HostPlayerSchema, PlayerModel, PlayerSchema
import json
from flask import Blueprint

# ルーティング設定
host_player_select = Blueprint("host_player_select", __name__)


@host_player_select.route("", methods=["POST"])
def selectHostPlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    try:
        select_host_player_list = HostPlayerModel.selectPlayerListOfHost(
            requested_data.get("host_id")
        )

        select_player_list = []
        for select_host_player in select_host_player_list:
            select_player_list.append(
                PlayerModel.selectPlayer(select_host_player.player_id)
            )
        player_schema = PlayerSchema(many=True)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_player_list": player_schema.dump(select_player_list),
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
