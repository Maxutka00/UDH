from django.db import models
from .topics import Topics


class News(models.Model):
    title = models.CharField(max_length=100)
    topics = models.ManyToManyField(Topics)
    url_shortcut = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    picture = models.BinaryField(null=True, blank=True)
    access = models.PositiveIntegerField()
    create_date = models.DateTimeField()

    @staticmethod
    def get_news_by_url_shortcut(url_shortcut: str):
        return News.objects.filter(url_shortcut=url_shortcut).first()
