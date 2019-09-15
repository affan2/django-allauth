from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path('^openid/login/$', views.login, name="openid_login"),
    re_path('^openid/callback/$', views.callback, name='openid_callback'),
]
