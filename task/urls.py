#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2019/1/4 15:16
# @Author  : WangKang

from django.conf.urls import url, include
from task import views
urlpatterns = [
    url(r'^record', views.record, name="record"),
    url(r'^details/(\d+)', views.details, name="details"),
]
