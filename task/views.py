from cmdb import models
from django.http import HttpResponse
from ansible_api.ans_api import MyRunner
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required   # 用户登录

import os
import json
import time


@login_required(login_url='/users/login/', redirect_field_name='next')
def record(request):
    record_objs = models.Record.objects.all().order_by('id')

    return render(request, "task/record.html", {"record_objs": record_objs})

def details(request, id):
    print(id)
    return HttpResponse(id)
