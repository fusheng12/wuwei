from cmdb import models
from django.http import HttpResponse
from ansible_api.ans_api import MyRunner
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required   # 用户登录

import os
import json
import time


@login_required(login_url='/users/login/', redirect_field_name='next')
def host(request):

    hosts_obj = models.Host.objects.all().order_by('id')
    # print(hosts_obj)
    return render(request, "cmdb/host.html", {"hosts_obj": hosts_obj})

@login_required(login_url='/users/login/', redirect_field_name='next')
def add_host(request):
    if request.method == "POST":
        print(request.POST)
        host_obj = models.Host(host_name=request.POST['hostname'], ip=request.POST['ip'], opm_name=request.POST['ompname'],
                                   assets_stauts=request.POST['assets_stauts'], idc=request.POST['idc'],
                                   remark=request.POST['remark'])
        copy_key = 'sshpass -p "%s" ssh-copy-id -i %s root@%s' % (request.POST['passwd'],
                                                                  '/root/.ssh/id_rsa.pub',
                                                                  request.POST['ip'])
        ip = request.POST['ip']
        ssh_key = os.system(copy_key)

        if ssh_key == 0:
            # 调用ansible api
            ansible = MyRunner(ip + ',')
            ansible.run(ip + ',', 'ping', '')
            result = ansible.get_result()
            if ip in json.dumps(result['success']):
                host_obj.host_status=0
                print("%s is ok!" % ip)
            else:
                print("ping loss!")

        host_obj.save()
        return redirect("/cmdb/host")
    return render(request, "cmdb/add_host.html",)