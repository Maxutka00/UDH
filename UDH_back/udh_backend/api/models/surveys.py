from django.db import models
from .users import Users


class Surveys(models.Model):
    members = models.ManyToManyField(Users)
    options = models.PositiveIntegerField()