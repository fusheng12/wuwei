from django.conf.urls import url, include
from file_issue import views
urlpatterns = [
    url(r'^upload', views.upload, name="upload"),
    url(r'^file', views.file, name="file"),
    url(r'index', views.index, name="index"),
]