import datetime

from flask import Blueprint, current_app, url_for
import jwt
from models.user import User
from config.database import db

from authlib.integrations.flask_client import OAuth

oauth_bp = Blueprint(
    "oauth_bp",
    __name__
)

oauth = OAuth()


def init_oauth(app):

    oauth.init_app(app)

    oauth.register(
        name="google",

        client_id=app.config["GOOGLE_CLIENT_ID"],

        client_secret=app.config["GOOGLE_CLIENT_SECRET"],

        server_metadata_url=
        "https://accounts.google.com/.well-known/openid-configuration",

        client_kwargs={
            "scope": "openid email profile"
        }
    )


@oauth_bp.route("/google")
def google_login():

    redirect_uri = url_for(
        "oauth_bp.google_callback",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri
    )


@oauth_bp.route("/google/callback")
def google_callback():

    token = oauth.google.authorize_access_token()

    user_info = token.get("userinfo")

    email = user_info["email"]

    name = user_info["name"]

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:

        user = User(
            email=email,
            name=name,
            provider="google"
        )

        db.session.add(user)
        db.session.commit()

    jwt_token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )


    return {
        "token": jwt_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "provider": user.provider
        }
        
    }
