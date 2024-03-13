from flask import request, make_response, jsonify, abort
from api.models import GameModel, GameSchema, HostModel
import json
from flask import Blueprint

# ルーティング設定
game_insert = Blueprint("game_insert", __name__)


@game_insert.route("", methods=["POST"])
def insertGame():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "game_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "host_id" in requested_data:
        abort(400, "host_id is a required!!")

    if not "game_title" in requested_data:
        abort(400, "game_title is a required!!")

    try:
        insert_game = GameModel.insertGame(requested_data)
        game_schema = GameSchema(many=False)

        host_data = HostModel.selectHost(requested_data.get("host_id"))

        game_host = {
            "host_id": requested_data.get("host_id"),
            "host_count": host_data.host_count + 1,
            "now_host": requested_data.get("game_id"),
        }
        HostModel.updateHost(game_host)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "insert_player": game_schema.dump(insert_game),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
