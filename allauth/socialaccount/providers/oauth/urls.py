from django.conf.urls import include, re_path

from allauth.utils import import_attribute


def default_urlpatterns(provider):
    login_view = import_attribute(
        provider.get_package() + '.views.oauth_login')
    callback_view = import_attribute(
        provider.get_package() + '.views.oauth_callback')

    urlpatterns = [
        re_path('^login/$',
            login_view, name=provider.id + "_login"),
        re_path('^login/callback/$', callback_view,
            name=provider.id + "_callback"),
    ]

    return [re_path('^' + provider.get_slug() + '/', include(urlpatterns))]
