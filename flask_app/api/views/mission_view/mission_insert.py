from flask import request, make_response, jsonify, abort
from api.models import MissionModel, MissionSchema
import json
from flask import Blueprint

# ルーティング設定
mission_insert = Blueprint("mission_insert", __name__)


@mission_insert.route("", methods=["POST"])
def insertMission():
    # jsonデータを取得する
    requested_json = json.dumps(request.json)
    requested_data = json.loads(requested_json)

    if not "mission_id" in requested_data:
        abort(400, "mission_id is a required!!")

    if not "mission_title" in requested_data:
        abort(400, "mission_title is a required!!")

    try:
        insert_mission = MissionModel.insertMission(requested_data)
        mission_schema = MissionSchema(many=False)
        return make_response(
            jsonify(
                {
                    "code": 200,
                    "insert_mission": mission_schema.dump(insert_mission),
                }
            )
        )
    except Exception as e:
        abort(400, e.args)
