import time

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods

from api.error_codes import ErrorCodes
from api.models.users import Users
from api.utils import token_funcs
from api.utils.utils import http_error


@require_http_methods(["POST"])
def log_in(request):
    """Required: login, password"""
    login = request.POST.get('login', None)
    password = request.POST.get('password', None)
    if not all((login, password)) or not (user := Users.authorize(login, password)):
        return http_error("Wrong login or password", 403)
    return JsonResponse({"status": 1, "data": {"token": user.get_token(), "timestamp": time.time()}}, status=200)


@require_http_methods(["POST"])
def register(request: WSGIRequest):
    """Required: login, password, name, email"""

    login = request.POST.get('login', None)
    password = request.POST.get('password', None)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    if not all((login, password, name, email)):
        return http_error("Not enough data", 403)
    user = Users.register_user(name, login, email, password)
    if user is None:
        return http_error("User exists", 403)
    else:
        return JsonResponse({"status": 1, "data": {"token": user.get_token(), "timestamp": time.time()}}, status=200)


