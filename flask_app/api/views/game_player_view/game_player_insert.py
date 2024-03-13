from flask import request, make_response, jsonify, abort
from api.models import GamePlayerModel, GamePlayerSchema, PlayerModel
import json
from flask import Blueprint

# ルーティング設定
game_player_insert = Blueprint("game_player_insert", __name__)


@game_player_insert.route("", methods=["POST"])
def insertGamePlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "game_id" in requested_data:
        abort(400, "game_id is a required!!")

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    # try:
    insert_game_player = GamePlayerModel.insertGamePlayer(requested_data)
    game_player_schema = GamePlayerSchema(many=False)

    player_data = PlayerModel.selectPlayer(requested_data.get("player_id"))

    game_player = {
        "player_id": requested_data.get("player_id"),
        "match_count": player_data.match_count + 1,
        "now_game": requested_data.get("game_id"),
    }
    PlayerModel.updatePlayer(game_player)
    response_player = {
        "game_id": requested_data.get("game_id"),
        "player_id": requested_data.get("player_id"),
        "player_name": player_data.player_name,
        "now_alive": insert_game_player.now_alive,
    }
    return make_response(
        jsonify(
            {
                "code": 200,
                "insert_player": response_player,
            }
        )
    )


# except Exception as e:
#     abort(400, e.args)
