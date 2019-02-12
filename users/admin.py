from django.contrib import admin
from .models import User

# 注册model 才能在admin中看到
admin.site.register(User)
