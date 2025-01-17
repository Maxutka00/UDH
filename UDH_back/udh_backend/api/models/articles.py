import random
import typing

from django.db import models
from django.db.models import QuerySet

from .topics import Topics
from .users import Users
from ..utils.utils import enforce_types


class Articles(models.Model):
    body = models.TextField()
    annotations = models.TextField()
    title = models.CharField(max_length=100)
    picture = models.BinaryField(null=True, blank=True)
    author = models.ManyToManyField(Users)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    topics = models.ManyToManyField(Topics)
    access = models.IntegerField()
    url_shortcut = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, blank=True, default=None)
    moderation_status = models.IntegerField()  # ???
    moderation_comment = models.TextField(null=True, blank=True)
    viewers_count = models.PositiveIntegerField(default=1)

    def user_granted_access(self, user: Users):
        if self.access == 1:
            authors = self.author.all()
            if user in authors:
                return True
            return False
        return True

    @classmethod
    def get_article_by_url_shortcut(cls, url_shortcut: str) -> "Articles":
        return cls.objects.filter(url_shortcut=url_shortcut).first()

    @staticmethod
    def is_article_exists_by_url_shortcut(url_shortcut: str):
        return bool(Articles.get_article_by_url_shortcut(url_shortcut))

    @classmethod
    def create_article(cls, body: str, annotations: str, title: str, picture: bytearray, access: int,
                       topics: list[Topics] | None, authors: list[Users]):
        article = cls()
        article.body = body
        article.annotations = annotations
        article.title = title
        article.picture = picture
        if topics:
            for topic in topics:
                topic.increment_view()
                topic.save()

        article.access = access
        # TODO: replace url_shortcut function
        url_shortcut = str(random.randint(10000000000000, 99999999999999999999999999))
        while cls.is_article_exists_by_url_shortcut(url_shortcut):
            url_shortcut = str(random.randint(10000000000000, 99999999999999999999999999))
        article.url_shortcut = url_shortcut
        article.moderation_status = 0
        article.save()
        article.author.set(authors)
        if topics:
            article.topics.set(topics)
        article.save()
        return article
