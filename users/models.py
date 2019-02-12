from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
    AbstractUser: 内置的User对象,用于记录用户的用户名，密码等个人信息
    Attributes: username,password,email,first_name,last_name
    '''
    nickname = models.CharField(max_length=50, blank=True)
    # mobilephone = models.IntegerField(blank=True, unique=True)

    class Meta(AbstractUser.Meta):
        pass