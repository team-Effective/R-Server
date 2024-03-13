from flask import request, make_response, jsonify, abort
from api.models import PlayerModel, PlayerSchema
import json
from flask import Blueprint

# ルーティング設定
player_update = Blueprint("player_update", __name__)


@player_update.route("", methods=["POST"])
def updatePlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "player_name" in requested_data:
        abort(400, "player_name is a required!!")

    try:
        update_player = PlayerModel.updatePlayer(requested_data)
        player_schema = PlayerSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_player": player_schema.dump(update_player),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
