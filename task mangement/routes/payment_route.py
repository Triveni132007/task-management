from flask import Blueprint
from flask import render_template
from services.map_service import get_branches_service


map_bp = Blueprint(
    "map_bp",
    __name__
)


@map_bp.route("/")
def map_page():

    branches = get_branches_service()

    return render_template(
        "map.html",
        branches=branches
    )