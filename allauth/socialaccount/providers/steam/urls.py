from django.conf.urls import re_path

from . import views


urlpatterns = [
    re_path("^steam/login/$", views.steam_login, name="steam_login"),
    re_path("^steam/callback/$", views.steam_callback, name="steam_callback"),
]
