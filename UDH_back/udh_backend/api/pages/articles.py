import os
import random

from django.core.handlers.wsgi import WSGIRequest
from django.http import QueryDict, JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from api.error_codes import ErrorCodes
from api.models import Users, articles, Articles, Topics
from api.status import StatusEnumerator
from api.utils.permission_flags import PermissionFlags
from api.utils.token_funcs import via_token
from api.utils.utils import http_error


@require_http_methods(["POST"])
@via_token(required_token=False)
def get_article(request: WSGIRequest, user: Users):
    post_request: QueryDict = request.POST
    article_id = post_request.get("article-id")
    article = Articles.get_article_by_url_shortcut(article_id)
    if not article:
        return http_error("Wrong article id", 400)
    if not article.user_granted_access(user):
        return http_error("User has no permission to view the article.", 403)
    author: Users
    authors = [author.name for author in article.author.all()]
    return JsonResponse({"status": 1, "data": {
        "body": article.body, "annotations": article.annotations,
        "title": article.title, "author": authors,
        "rating": article.rating, "access": article.access,
        "create_date": article.create_date, "edit_date": article.edit_date,
        "moderation_comment": article.moderation_comment,
        "moderation_status": article.moderation_status,
        "viewers_count": article.viewers_count}}, status=200)


@require_http_methods(["POST",  "GET"])
@via_token(required_token=False)
def get_article_picture(request: WSGIRequest,  user: Users):
    post_request: QueryDict = request.POST
    article_id = post_request.get("article-id")
    article = Articles.get_article_by_url_shortcut(article_id)
    if not article:
        return http_error("Wrong article id", 400)
    if not article.user_granted_access(user):
        return http_error("User has no permission to view the article.", 403)

    return HttpResponse(article.picture, status=200)


@require_http_methods(["POST"])
@via_token()
def create_article(request: WSGIRequest, user: Users):
    # TODO: body shielding
    # TODO: config file
    max_body_len = int(os.getenv("ARTICLE_MAX_BODY_LEN"))
    max_annot_len = int(os.getenv("ARTICLE_MAX_ANNOT_LEN"))
    max_picture_size = int(os.getenv("ARTICLE_MAX_PICTURE_SIZE"))
    max_title_len = int(os.getenv("ARTICLE_MAX_TITLE_LEN"))

    post_request: QueryDict = request.POST
    body = post_request.get("body")
    annotations = post_request.get("annotations")
    title = post_request.get("title")
    picture = post_request.get("picture")
    access = post_request.get("access")
    raw_topics = post_request.getlist("topics")
    # TODO: how author will be implemented
    # author = post_request.get("author")
    authors = [user]


    if not all((body, annotations, title, picture, access)) or \
            not access.isdigit():
        return http_error("Invalid syntax", 400)
    access = int(access)
    picture = picture.encode()

    permissions = user.get_permissions()
    if not permissions.article_create:
        return http_error("User has no permission", 403)

    if len(body) > max_body_len \
            or len(annotations) > max_annot_len \
            or len(title) > max_title_len:
        return http_error("Invalid data length", 400)

    if isinstance(picture, bytearray):
        if len(picture) > max_picture_size:
            # TODO: implement 415 Unsupported Media Type
            return http_error("The picture attached is too big.", 400)
    topics = None
    if raw_topics:
        topics = Topics.parse_topics(raw_topics)
    if topics == StatusEnumerator.DataTooLong:
        return http_error("Invalid data length (topics)", 400)
    article = Articles.create_article(body, annotations, title, picture, access, topics, authors)

    return JsonResponse({"status": 1, "data": {"url-shortcut": article.url_shortcut}}, status=200)
