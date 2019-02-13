from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class Host(models.Model):
    HOST_STATUS = ((0, '正常'), (1, '不可达'))
    ASSET_STATUS = ((0, '在线'), (1, '测试'), (2, '闲置'), (3, '保修'))
    host_name=models.CharField(max_length=64)
    ip=models.CharField(max_length=32, null=False)
    host_status=models.IntegerField(choices=HOST_STATUS, default=1)
    assets_stauts=models.IntegerField(choices=ASSET_STATUS)
    opm_name=models.CharField(max_length=32, null=False)
    idc=models.CharField(max_length=64)
    time=models.DateTimeField(default=timezone.now)
    remark=models.CharField(max_length=128) # 备注

    def __unicode__(self):
        return self.host_name

class Record(models.Model):
    '''操作记录表'''
    hosts =  models.TextField(null=False)
    module = models.CharField(max_length=32, null=False)
    module_args = models.CharField(max_length=128)
    result = models.TextField(default="")
    time = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.hosts