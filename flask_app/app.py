# -*- coding: utf-8 -*-
from flask import Flask
from api import app
from dotenv import load_dotenv
from flask import request, make_response, jsonify, abort
import json

load_dotenv()
import os

PORT = os.getenv("PORT")


@app.route("/")
def index():
    return "It works!"


@app.errorhandler(Exception)
def error_handler(err):
    res = jsonify(
        {"error": {"name": err.name, "description": err.description}, "code": err.code}
    )
    return res, err.code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, threaded="true")
