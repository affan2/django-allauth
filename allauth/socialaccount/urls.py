from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^login/cancelled/$', views.login_cancelled,
        name='socialaccount_login_cancelled'),
    re_path(r'^login/error/$', views.login_error,
        name='socialaccount_login_error'),
    re_path(r'^signup/$', views.signup, name='socialaccount_signup'),
    re_path(r'^connections/$', views.connections, name='socialaccount_connections')
]
