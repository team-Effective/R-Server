from flask import request, make_response, jsonify, abort
from api.models import GameModel, GameSchema
import json
from flask import Blueprint

# ルーティング設定
game_select = Blueprint("game_select", __name__)


@game_select.route("/host", methods=["POST"])
def selectGameListOfHost():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "host_id" in requested_data:
        abort(400, "host_id is a required!!")

    try:
        select_game_list = GameModel.selectGameListOfHost(requested_data.get("host_id"))
        game_schema = GameSchema(many=True)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_game_list": game_schema.dump(select_game_list),
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


@game_select.route("/once", methods=["POST"])
def selectGameOnce():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "game_id" in requested_data:
        abort(400, "game_id is a required!!")

    try:
        select_game = GameModel.selectGameOnce(requested_data.get("game_id"))
        game_schema = GameSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_game": game_schema.dump(select_game),
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
