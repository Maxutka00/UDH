import os.path

from django.http import HttpResponse
from django.test import TestCase
from django.views.decorators.http import require_http_methods

from api.models import articles


# Create your tests here.


@require_http_methods(["GET"])
def create_article_view(request):
    with open(os.path.join("..", "tests", "www", "articles.html"), "r") as f:
        return HttpResponse(f.read())

@require_http_methods(["GET"])
def register_view(request):
    with open(os.path.join("..", "tests", "www", "register.html"), "r") as f:
        return HttpResponse(f.read())

@require_http_methods(["GET"])
def article_view(request, id_: int):
    article: articles.Articles | None = articles.Articles.objects.filter(url_shortcut=id_).first()
    if article is None:
        return HttpResponse("Article not found", status=404)
    with open(os.path.join("..", "tests", "www", "show_article.html"), "r") as f:
        # <h1>{title}</h1>
        #     <h4>{annotations}</h4>
        #     <h5>{body}</h5>
        #     <img src="/{id}/image" alt="image">
        #     <h6>Access: {access}</h6>
        picture = "<span>No picture</span>"
        if article.picture:
            picture = f'<img src="image/" alt="image">'
        return HttpResponse(f.read().format(article.title, article.annotations, article.body, picture, article.access,
                                            article.create_date))


@require_http_methods(["GET"])
def article_image_view(request, id_: int):
    article: articles.Articles | None = articles.Articles.objects.filter(url_shortcut=id_).first()
    if article is None:
        return HttpResponse("Article not found", status=404)
    if article.picture:
        return HttpResponse(article.picture)
    return HttpResponse("No photo", status=404)
