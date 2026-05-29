import jwt
import datetime
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from config.database import db
from models.user import User


def signup_service(data):
    """Create a new user. Returns (response_dict, status_code)."""
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"message": "Username and password are required"}, 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {"message": "Username already exists"}, 400

    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)

    db.session.add(user)
    db.session.commit()
    return {"message": "User created successfully"}, 201


def _generate_token(user_id, expires_hours=2):
    """Return a JWT for given user_id."""
    secret = current_app.config.get("SECRET_KEY", "dev-secret")
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expires_hours),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    # PyJWT>=2 returns str, older versions return bytes
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def _decode_token(token):
    """Decode token and return payload or raise an exception."""
    secret = current_app.config.get("SECRET_KEY", "dev-secret")
    return jwt.decode(token, secret, algorithms=["HS256"])


def login_service(data):
    """Authenticate user and return JWT on success."""
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return {"message": "Username and password are required"}, 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"message": "Invalid username or password"}, 401
    if not check_password_hash(user.password, password):
        return {"message": "Invalid username or password"}, 401

    token = _generate_token(user.id)
    return {"token": token}, 200


def get_user_from_token(token):
    """Return User instance for a valid token, or (message, status) on error."""
    try:
        payload = _decode_token(token)
    except jwt.ExpiredSignatureError:
        return {"message": "Token expired"}, 401
    except jwt.InvalidTokenError:
        return {"message": "Invalid token"}, 401

    user_id = payload.get("user_id")
    if not user_id:
        return {"message": "Invalid token payload"}, 401

    user = User.query.get(user_id)
    if not user:
        return {"message": "User not found"}, 404

    return user