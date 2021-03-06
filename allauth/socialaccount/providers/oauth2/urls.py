from django.conf.urls import url, include
from allauth.utils import import_attribute


def default_urlpatterns(provider):
    login_view = import_attribute(
        provider.get_package() + '.views.oauth2_login')
    callback_view = import_attribute(
        provider.get_package() + '.views.oauth2_callback')

    urlpatterns = [
        url('^login/$', login_view,
            name=provider.id + '_login'),
        url('^login/callback/$', callback_view,
            name=provider.id + '_callback'),
    ]

    try:
        logout_view = import_attribute(
            provider.get_package() + '.views.oauth2_logout')
    except (ImportError, AttributeError):
        logout_view = None

    try:
        callback_logout_view = import_attribute(
            provider.get_package() + '.views.oauth2_callback_logout')
    except (ImportError, AttributeError):
        callback_logout_view = None

    if logout_view is not None:
        urlpatterns += [
            url('^logout/$', logout_view,
                name=provider.id + '_logout'),
        ]
    if callback_logout_view is not None:
        urlpatterns += [
            url('^logout/callback/$', callback_logout_view,
                name=provider.id + '_callback_logout'),
        ]

    return [url('^' + provider.id + '/', include(urlpatterns))]
