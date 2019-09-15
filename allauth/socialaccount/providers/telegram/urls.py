from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path('^telegram/login/$', views.telegram_login, name="telegram_login")
]
