from django.core.handlers.wsgi import WSGIRequest
import inspect
import os
from functools import wraps
from typing import Callable

from django.http import JsonResponse

from api.models import Users, Articles, Comments


def is_multi_instance(_types: type, *instances):
    for instance in instances:
        if not isinstance(instance, _types):
            return False
    return True


def get_data(f):
    def wrapper(*args, **kwargs):
        request: WSGIRequest | None = None
        for arg in args:
            if isinstance(arg, WSGIRequest):
                request: WSGIRequest = arg
        if request is None:
            raise Exception("Invalid get_data usage!")
        r = request.POST
        if login := r.get("login"):
            kwargs.update({"user": Users.get_user(login)})
        if url_article := r.get("url_article"):
            kwargs.update({"article": Articles.get_article_by_url_shortcut(url_article)})
        if url_news := r.get("url_news"):
            kwargs.update({"news": Articles.get_article_by_url_shortcut(url_news)})
        if comment_id := r.get("comment_id"):
            kwargs.update({"comment": Comments.get_comment(comment_id)})
        print(args, kwargs)
        return f(*args, **kwargs)

    return wrapper


def http_error(error: str, status=None):
    return JsonResponse({"status": 0, "error": error}, status=status)
def http_error(error: str, status=None):
    return JsonResponse({"status": 0, "error": error}, status=status)

def environment_checkup():
    # If any raise an error - environment checkup failed
    int(os.getenv("ARTICLE_MAX_BODY_LEN"))
    int(os.getenv("ARTICLE_MAX_ANNOT_LEN"))
    int(os.getenv("ARTICLE_MAX_PICTURE_SIZE"))
    int(os.getenv("ARTICLE_MAX_TITLE_LEN"))


def enforce_types(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        annotations = inspect.get_annotations(func)
        for arg, value, arg_name in zip(annotations.values(), args, annotations.keys()):
            if not isinstance(value, arg):
                raise TypeError(f"Expected {arg} for {value} (arg name: {arg_name})")
        for arg, value in kwargs.items():
            if not isinstance(value, annotations[arg]):
                raise TypeError(f"Expected {annotations[arg]} for {value}")
        return func(*args, **kwargs)
    return wrapper
