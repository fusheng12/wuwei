#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/2/12 11:01
# @Author  : WangKang

from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
