from passlib.hash import bcrypt
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from http import HTTPStatus


def hash_password(plain_text):
    hashed_password = bcrypt.using(rounds=13).hash(plain_text)
    return hashed_password


def verify_password(plain_text, hashed_password):
    return bcrypt.verify(plain_text, hashed_password)


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == "admin":
                return fn(*args, **kwargs)
            else:
                return {"message": "Admin only"}, HTTPStatus.FORBIDDEN

        return decorator

    return wrapper
