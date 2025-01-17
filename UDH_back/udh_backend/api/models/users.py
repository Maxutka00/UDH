import os
import time
import typing
import uuid

import jwt
from django.db import models
import hashlib
from api.utils.permission_flags import PermissionFlags


class Users(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    login = models.CharField(max_length=50)
    password = models.TextField()  # hash
    salt = models.TextField(default="")
    avatar = models.BinaryField(null=True, blank=True)
    rsa_key = models.TextField(null=True, blank=True)
    roles = models.IntegerField(default=0)  # PermissionFlags
    google_token = models.CharField(max_length=256, null=True, blank=True)

    def get_token(self):
        self.login: str
        self.password: str
        self.salt: str
        dict_usr = {'salt': str(time.time()), 'login': self.login, 'user_password':
            self.password, "expired": int(time.time() + 28 * 24 * 60 * 60)}
        return jwt.encode(dict_usr, os.getenv("TOKEN_KEY"), algorithm='HS256')

    def get_permissions(self):
        self.roles: int
        return PermissionFlags(self.roles)

    def __str__(self):
        return f"{self.login}:{self.password}"

    @classmethod
    def filter_user(cls, **kwargs) :
        return cls.objects.filter(**kwargs)

    @staticmethod
    def get_user(login: str):
        return Users.filter_user(login=login.lower()).first()
    @classmethod
    def user_exists(cls, **kwargs):
        return cls.filter_user(**kwargs).exists()

    @classmethod
    def check_password(cls, login: str, password: str):
        return bool(cls.authorize(login, password))

    @staticmethod
    def check_user(**kwargs):
        return Users.filter_user(**kwargs).exists()

    @classmethod
    def authorize(cls, login: str, password: str) -> typing.Union[None, "Users"]:
        login = login.lower()
        user = cls.get_user(login)
        salt: str = user.salt
        if not user:
            return None
        hashed_password = cls.hash_password(password, salt)
        if user.password == hashed_password:
            return user
        else:
            return None

    @classmethod
    def hash_password(cls, password: str, salt: str):
        return hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

    @classmethod
    def register_user(cls, name: str, login: str, email: str, password: str):
        login = login.lower()
        email = email.lower()
        if cls.user_exists(login=login, email=email):
            return None

        permissions = PermissionFlags.default_user()

        user = cls(name=name, email=email, login=login, roles=permissions.serialize(), avatar=None, rsa_key=None,
                   google_token=None)
        user.salt = uuid.uuid4().hex
        user.password = cls.hash_password(password, user.salt)
        user.save()
        return user


def make_hash(password: str, salt: str):
    return hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()


