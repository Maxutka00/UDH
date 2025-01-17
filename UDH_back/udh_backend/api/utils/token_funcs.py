import os
import time
from functools import wraps
import inspect
import jwt
from django.core.handlers.wsgi import WSGIRequest

from api.error_codes import ErrorCodes
from api.models.users import Users
from api.status import StatusEnumerator
from api.utils.utils import http_error


def create_token(login: str, password: str):
    dict_usr = {'salt': str(time.time()), 'login': str(login), 'user_password': str(password),
                "expired": int(time.time() + 60 * 24 * 60 * 60)}
    return jwt.encode(dict_usr, os.getenv("TOKEN_KEY"), algorithm='HS256')


def decode_token(token: str) -> dict:
    return jwt.decode(token, os.getenv("TOKEN_KEY"), algorithms=['HS256'])


def check_token(token: str, user: Users) -> StatusEnumerator:
    decoded = decode_token(token)
    expired: int = decoded.get("expired")
    login: str = decoded.get("login").lower()
    password: str = decoded.get("user_password")
    # password = Users.hash_password(password, user.salt)
    if user.login != login:
        return StatusEnumerator.UserLoginDoesNotMatch
    if user is None:
        return StatusEnumerator.UserDoesNotExists
    if user.password != password:
        return StatusEnumerator.UserInvalidToken
    if expired < time.time():
        return StatusEnumerator.UserTokenExpired
    return StatusEnumerator.UserSuccess


def get_user(token: str) -> StatusEnumerator | Users:
    decoded = decode_token(token)
    login: str = decoded.get("login")
    user: Users = Users.get_user(login=login)
    if user is None:
        return StatusEnumerator.UserDoesNotExists
    return user


def invalid_token(_: WSGIRequest = None):
    return http_error("Invalid token", 403)


def via_token(required_token=True, invalid_callback: callable = invalid_token, *jargs, **jkwargs):
    """param: invalid_callback is the function which execute after the check_token fail; Use param with the annotation
    users.User to get the user as a param"""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request: WSGIRequest | None = None
            for arg in args:
                if isinstance(arg, WSGIRequest):
                    request: WSGIRequest = arg
            if request is None:
                raise Exception("Invalid via_token usage!")
            token = request.headers.get("Authorization")
            token: None | str
            if token is not None and token.startswith("Basic"):
                if len(token_split := token.split()) == 2:
                    token = token_split[1]
                    user = get_user(token)
                    if isinstance(user,StatusEnumerator):
                        return invalid_callback(*args, **kwargs)
                    if (isinstance(user, Users) and check_token(token, user) == StatusEnumerator.UserSuccess) \
                            or not required_token:
                        kwargs["user"] = user

                        return f(*args, *jargs, **kwargs, **jkwargs)
            if not required_token:
                kwargs["user"] = None
                return f(*args, *jargs, **kwargs, **jkwargs)
            if invalid_callback is not None:
                return invalid_callback(*args, **kwargs)

        return wrapper

    return decorator
