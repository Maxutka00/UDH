import random
import time
from typing import Union

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import JsonResponse, QueryDict
from django.views.decorators.http import require_http_methods

from api.error_codes import ErrorCodes
from api.models import users, articles, topics, Articles, Users, Comments, Topics
from api.status import StatusEnumerator
from api.utils import token_funcs
from api.utils.permission_flags import PermissionFlags
from api.utils.token_funcs import via_token
from api.utils.utils import http_error, get_data


@require_http_methods(["POST"])
def log_in(request):
    """User should store token at the Header::Authorization: Basic
     Watch: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization"""
    login = request.POST.get('login', None)
    password = request.POST.get('password', None)
    if None not in (login, password) and Users.check_password(login, password):
        t = token_funcs.create_token(login, password)
        return JsonResponse({"status": 1, "data": {"token": t, "timestamp": time.time()}}, status=200)
    else:
        return http_error("Wrong login or password", 403)


@require_http_methods(["POST"])
def register(request: WSGIRequest):
    login = request.POST.get('login', None)
    password = request.POST.get('password', None)
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    if None in (login, password, name, email):
        return http_error("Not enough data", 400)
    answer = Users.register_user(name, login, email, password)
    if not answer:
        return http_error("User exists", 400)
    else:
        t = token_funcs.create_token(login, password)
        return JsonResponse({"status": 1, "data": {"token": t, "timestamp": time.time()}}, status=200)


@require_http_methods(["POST"])
@via_token()
def test_token(request: WSGIRequest):
    return JsonResponse({"status": 1, "message": "Successfully!"}, status=200)


@require_http_methods(["POST"])
@via_token()
def create_article(request: WSGIRequest, user: Users):
    # TODO: body shielding
    body_len = 15_000
    annot_len = 1500
    picture_size = (2 ** 6) * 2  # 2 megabytes
    title_len = 100
    post_request: QueryDict = request.POST
    body = post_request.get("body")
    annotations = post_request.get("annotations")
    title = post_request.get("title")
    picture: InMemoryUploadedFile = request.FILES.get("picture")
    # TODO: how author will be implemented
    # author = post_request.get("author")
    authors = [user]
    access = post_request.get("access")
    raw_topics = post_request.getlist("topics")

    if None in (body, annotations, title, picture, access, raw_topics) or \
            not access.isdigit() or not isinstance(raw_topics, list):
        return http_error("Invalid syntax", 400)
    picture = picture.open().read()
    permissions = PermissionFlags(user.roles)

    if not (permissions.user and permissions.article_create):
        return http_error("User has no permit", 403)

    access = int(access)

    if len(body) > body_len \
            or len(annotations) > annot_len \
            or len(title) > title_len:
        return http_error("Invalid data length", 400)

    if isinstance(picture, bytearray):
        if len(picture) > picture_size:
            return http_error("The picture attached is too big.", 400)

    article = articles.Articles()
    article.body = body
    article.annotations = annotations
    article.title = title
    article.picture = picture
    topics = []
    for raw_topic in raw_topics:
        topic = Topics.get_topic(raw_topic)
        if not topic:
            topic = Topics.create_topic(raw_topic)
            if isinstance(topic, StatusEnumerator):
                if topic == StatusEnumerator.DataTooLong:
                    return http_error("Invalid data length (topics)", 400)
        topics.append(topic)

    for topic in topics:
        topic.increment_view()
        topic.save()

    article.access = access

    url_shortcut = str(random.randint(10000000000000, 99999999999999999999999999))
    while Articles.is_article_exists_by_url_shortcut(url_shortcut):
        url_shortcut = str(random.randint(10000000000000, 99999999999999999999999999))
    article.url_shortcut = url_shortcut
    article.moderation_status = 0
    article.save()
    article.author.set(authors)
    article.author.set([user])
    article.topics.set(topics)
    article.save()

    return JsonResponse({"status": 1, "data": {"url-shortcut": url_shortcut}}, status=200)


@require_http_methods(["POST"])
@via_token()
@get_data
def comment_article(request: WSGIRequest, user: Users, article: Articles, comment: Comments = None):
    if None in (article, user):
        return http_error("Invalid data or not enough data", 400)
    post_request: QueryDict = request.POST
    text = post_request.get("text")
    rating = post_request.get("rating")
    if len(text) > 1000:
        return http_error("Comment text too long", 400)
    Comments.add_comment(user, article, text, rating, comment)
    return JsonResponse({"status": 1}, status=200)


@require_http_methods(["POST"])
@via_token()
@get_data
def edit_comment(request: WSGIRequest, user: QuerySet, comment: Union[Comments, QuerySet]):
    if not user:
        return http_error("Invalid data or not enough data", 400)
    post_request: QueryDict = request.POST
    text = post_request.get("text")
    if comment.author != user:
        return http_error("User has no permit", 403)
    if len(text) > 1000:
        return http_error("Comment text too long", 400)
    Comments.edit_comment(comment, text)
    return JsonResponse({"status": 1}, status=200)
