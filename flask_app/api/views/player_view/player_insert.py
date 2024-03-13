from flask import request, make_response, jsonify, abort
from api.models import PlayerModel, PlayerSchema
import json
from flask import Blueprint

# ルーティング設定
player_insert = Blueprint("player_insert", __name__)


@player_insert.route("", methods=["POST"])
def insertPlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "player_name" in requested_data:
        abort(400, "player_name is a required!!")

    try:
        insert_player = PlayerModel.insertPlayer(requested_data)
        player_schema = PlayerSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "insert_player": player_schema.dump(insert_player),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
