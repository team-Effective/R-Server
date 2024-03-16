from flask import request, make_response, jsonify, abort
from api.models import PlayerModel, PlayerSchema
import json
from flask import Blueprint

# ルーティング設定
player_select = Blueprint("player_select", __name__)


@player_select.route("", methods=["POST"])
def selectPlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    try:
        select_player = PlayerModel.selectPlayer(requested_data.get("player_id"))
        player_schema = PlayerSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_player": player_schema.dump(select_player),
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
