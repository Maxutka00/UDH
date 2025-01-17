from typing import Union

from django.db import models
from .users import Users
from .articles import Articles
from .news import News


class Comments(models.Model):
    author = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, null=True, blank=True)
    answer_to = models.ForeignKey("Comments", on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveIntegerField()
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(null=True, blank=True, auto_now=True)

    @staticmethod
    def add_comment(author: Users, root: Union[Articles, News], text: str, rating: int, answer_to: "Comments" = None):
        comment = Comments(author=author, text=text, rating=rating, answer_to=answer_to)
        if isinstance(root, Articles):
            comment = Comments(author=author, article=root, text=text, rating=rating, answer_to=answer_to)
            comment.article = root
            root_type = 0
        else:
            comment.news = root
            root_type = 1
        comment.save()
        if root_type == 0:
            r = Comments.objects.filter(article__id=root.id).aggregate(models.Avg('rating'))
        else:
            r = Comments.objects.filter(news__name=root).aggregate(models.Avg('rating'))
        root.rating = r['rating__avg']
        root.save()

    @staticmethod
    def edit_comment(comment: models.query.QuerySet, text: str):
        comment.update(text=text)

    @staticmethod
    def get_comment(comment_id: int):
        return Comments.objects.filter(id=comment_id).first()