"""
Copyright 2022 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""

from flask import Blueprint, jsonify, request, current_app
from pyrender.interface import MessageProtocol, IRenderData
from datetime import datetime, timedelta
from pyrender.http_service.service import Webbrowser


api_bp = Blueprint('api_route', __name__, url_prefix="/page")


@api_bp.route("/render", methods=["GET", "POST"])
def render():

    clear_time = int((datetime.now() + timedelta(seconds=60 * 5)).timestamp())

    url = None
    wait = None
    jscript = None
    web_wait = None

    if request.args:
        url = request.args.get("url")
        wait = request.args.get("wait")
        jscript = request.args.get("jscript")
        web_wait = request.args.get("web_wait")

    if request.form:
        url = request.form.get("url")
        wait = request.form.get("wait")
        jscript = request.form.get("jscript")
        web_wait = request.args.get("web_wait")

    if request.data:
        data = request.json
        url = data.get('url')
        wait = data.get('wait')
        jscript = data.get('jscript')
        web_wait = data.get('web_wait')

    if url is None:
        raise ValueError(f"Error Url: <{url}>")

    message = MessageProtocol(
        action="render", payload={
            "url": url,
            "wait": wait,
            "expiration_date": clear_time,
            "jscript": jscript,
            "web_wait": web_wait
        }
    )
    task_id = Webbrowser.render(message, current_app.config)
    return jsonify(MessageProtocol(payload=[task_id]).to_dict())


@api_bp.route("/result/<keyid>", methods=["GET"])
def get_result(keyid):
    message = MessageProtocol(payload={
        "id": keyid,
    }, action="result")
    result: IRenderData = Webbrowser.result(message, current_app.config)
    return jsonify(MessageProtocol(payload=[result.to_dict()]).to_dict())


@api_bp.route("/live", methods=["GET", "POST"])
def active_content():
    wait = None
    jscript = None

    if request.args:
        wait = request.args.get("wait")
        jscript = request.args.get("jscript")

    if request.form:
        wait = request.form.get("wait")
        jscript = request.form.get("jscript")

    message = MessageProtocol(action="active_content", payload={
        "wait": wait,
        "jscript": jscript
    })
    response: IRenderData = Webbrowser.live(message, current_app.config)
    return jsonify(MessageProtocol(payload=[response.to_dict()]).to_dict())
