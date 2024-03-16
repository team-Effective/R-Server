from flask import request, make_response, jsonify, abort
from api.models import (
    GameModel,
    GameSchema,
    GamePlayerModel,
    PlayerModel,
    HostModel,
)
import json
from flask import Blueprint

# ルーティング設定
game_update = Blueprint("game_update", __name__)


@game_update.route("/finish", methods=["POST"])
def updateGameFinish():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "game_id" in requested_data:
        abort(400, "game_id is a required!!")

    try:
        select_player_list_of_game = GamePlayerModel.selectPlayerListOfGame(
            requested_data.get("game_id")
        )
        for select_game_player in select_player_list_of_game:
            select_player = PlayerModel.selectPlayer(select_game_player.player_id)
            if select_game_player.now_alive == True:
                PlayerModel.updatePlayer(
                    {
                        "player_id": select_player.player_id,
                        "alive_count": select_player.alive_count + 1,
                        "now_game": None,
                    }
                )
            else:
                PlayerModel.updatePlayer(
                    {
                        "player_id": select_player.player_id,
                        "now_game": None,
                    }
                )
        select_game = GameModel.selectGameOnce(requested_data.get("game_id"))
        HostModel.updateHost(
            {
                "host_id": select_game.host_id,
                "now_host": None,
            }
        )
        player_schema = GameSchema(many=False)

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "update_game_finish": player_schema.dump(select_game),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
