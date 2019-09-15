from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path('^draugiem/login/$', views.login, name="draugiem_login"),
    re_path('^draugiem/callback/$', views.callback, name='draugiem_callback'),
]
