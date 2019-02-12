import os

# from ansible_api.ans_api import MyRunner
from django.shortcuts import render, redirect
from django.http import HttpResponse
from file_issue.common import file_info
from django.contrib.auth.decorators import login_required   # 用户登录
###########################
path = "file_issue/upload/"

###########################

@login_required(login_url='/users/login/', redirect_field_name='next')
def upload(request):
    # print("上传文件！")
    file_dict = {}
    file_list = os.listdir(path)
    n = 1
    for file in file_list:
        info = file_info(path + file)
        info.insert(0, str(file))
        file_dict[n] = info
        n+=1

    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None

        if not myFile:
            return HttpResponse("no files for upload!")

        destination = open(path + myFile.name, 'wb+') # 新建文件
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("Upload file: %s    size: %s" % (myFile.name, myFile.size))

    # print(file_dict)
    return render(request, "file_issue/file_up.html", {"file_dict": file_dict,})

@login_required(login_url='/users/login/', redirect_field_name='next')
def file_list(request):
    return render(request, "file_issue/file_list.html", )

@login_required(login_url='/users/login/', redirect_field_name='next')
def file(request):
    if request.method == "POST":
        print("开始分发...")
        print(request.POST)
        ip = request.POST['ip']
        src_name = request.POST['src_name']
        dst = request.POST['dst']
        #return HttpResponse("{'SUCCESS': 'OK'}")
        if ip != "" and src_name != "" and dst!= "":
            if os.path.exists(path + src_name):
                print(ip, src_name, dst)

                # 调用ansible api
                # ansible = MyRunner(ip + ',')
                # 结果
                # ansible.run(ip + ',', 'copy', 'src=%s%s dest=%s' % (path, src_name, dst))
                # result = ansible.get_result()
                # print(result)
                return HttpResponse("Files %s issue Success!\n" % src_name)

            else:
                return HttpResponse("Files %s is not exist!" % src_name)
    return render(request, "file_issue/file_issue.html")

@login_required(login_url='/users/login/', redirect_field_name='next')
def index(request):
    return render(request, "registration/l.html")

