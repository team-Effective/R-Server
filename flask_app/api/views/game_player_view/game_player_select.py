from flask import request, make_response, jsonify, abort
from api.models import GamePlayerModel, GamePlayerSchema, PlayerModel, PlayerSchema
import json
from flask import Blueprint

# ルーティング設定
game_player_select = Blueprint("game_player_select", __name__)


@game_player_select.route("/game", methods=["POST"])
def selectPlayerListOfGame():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    try:
        select_player_list_of_game = GamePlayerModel.selectPlayerListOfGame(
            requested_data.get("game_id")
        )
        select_game_player_list = []
        for select_game_player in select_player_list_of_game:
            player_data = PlayerModel.selectPlayer(select_game_player.player_id)
            select_game_player_list.append(
                {
                    "game_id": select_game_player.game_id,
                    "player_id": select_game_player.player_id,
                    "player_name": player_data.player_name,
                    "now_alive": select_game_player.now_alive,
                }
            )

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_game_player_list": select_game_player_list,
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


@game_player_select.route("/once", methods=["POST"])
def selectGamePlayer():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    try:
        select_game_player = GamePlayerModel.selectGamePlayer(requested_data)
        player_data = PlayerModel.selectPlayer(select_game_player.player_id)
        response_game_player = {
            "game_id": select_game_player.game_id,
            "player_id": select_game_player.player_id,
            "player_name": player_data.player_name,
            "now_alive": select_game_player.now_alive,
        }

        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_game_player": response_game_player,
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
