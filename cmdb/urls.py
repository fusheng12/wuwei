#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 15:16
# @Author  : WangKang

from django.conf.urls import url, include
from cmdb import views
urlpatterns = [
    url(r'^host', views.host, name="host"),
    url(r'^add_host', views.add_host, name="add_host"),
]
