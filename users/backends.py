#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/2/12 15:11
# @Author  : WangKang

from .models import User

class EmailBackend(object):
    def authenticate(self, request, **credentials):
        # 要注意登录表单中用户输入的用户名或者邮箱的 field 名均为 username
        print("=====================")
        email = credentials.get('email', credentials.get('username'))
        try:
            # get方法在有多个email相同时会报错
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        """
        该方法是必须的
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None