"""
URL configuration for udh_backend project.

The `urlpatterns` list routes URLs to pages. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function pages
    1. Add an import:  from my_app import pages
    2. Add a URL to urlpatterns:  path('', pages.home, name='home')
Class-based pages
    1. Add an import:  from other_app.pages import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from api.pages import articles
from api.pages import authorization
from api.pages import views, tests

def api_v1(path_: str):

    return "api/v1/" + path_


urlpatterns = [
    path(api_v1('admin/'), admin.site.urls),
    path(api_v1("login/"), authorization.log_in),
    path(api_v1("register/"), authorization.register),
    path(api_v1('test_token/'), views.test_token),
    path(api_v1('create_article/'), views.create_article),
    path(api_v1('comment_article/'), views.comment_article),
    path(api_v1('edit_comment/'), views.edit_comment),
    path(api_v1("create_article/"), articles.create_article),
    path(api_v1("get_article_picture/"), articles.get_article_picture),
    path(api_v1("get_article/"), articles.get_article),
]

