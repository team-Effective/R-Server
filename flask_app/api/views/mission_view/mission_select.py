from flask import request, make_response, jsonify, abort
from api.models import MissionModel, MissionSchema
import json
from flask import Blueprint

# ルーティング設定
mission_select = Blueprint("mission_select", __name__)


@mission_select.route("", methods=["POST"])
def selectMission():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    try:
        select_mission = MissionModel.selectMission(requested_data.get("mission_id"))
        mission_schema = MissionSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "select_mission": mission_schema.dump(select_mission),
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
