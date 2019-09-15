from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path('^persona/login/$', views.persona_login, name="persona_login")
]
