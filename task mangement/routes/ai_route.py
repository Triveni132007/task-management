from flask import Blueprint
from flask import request
from flask import jsonify
from flask import render_template

from services.ai_service import (
    ask_ai_service
)


ai_bp = Blueprint(
    "ai_bp",
    __name__
)


@ai_bp.route("/")
def ai_ui():

    return render_template(
        "ai.html"
    )


@ai_bp.route("/ask", methods=["POST"])
def ask_ai():

    message = request.json["message"]

    response = ask_ai_service(
        message
    )

    return jsonify({
        "reply": response
    })