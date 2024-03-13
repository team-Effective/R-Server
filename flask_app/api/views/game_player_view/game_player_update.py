from flask import request, make_response, jsonify, abort
from api.models import GamePlayerModel, GamePlayerSchema
import json
from flask import Blueprint

# ルーティング設定
game_player_update = Blueprint("game_player_update", __name__)


@game_player_update.route("/death", methods=["POST"])
def updateGamePlayerDeath():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "player_id" in requested_data:
        abort(400, "player_id is a required!!")

    if not "game_id" in requested_data:
        abort(400, "game_id is a required!!")

    try:
        update_player = {
            "game_id": requested_data.get("game_id"),
            "player_id": requested_data.get("player_id"),
            "now_alive": False,
        }
        update_game_player_death = GamePlayerModel.updateGamePlayer(update_player)
        player_schema = GamePlayerSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_game_player_death": player_schema.dump(
                        update_game_player_death
                    ),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
