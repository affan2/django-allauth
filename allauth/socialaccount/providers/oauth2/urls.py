from django.conf.urls import patterns, url, include
from django.utils.module_loading import import_string


def default_urlpatterns(provider):
    package = provider.get_package()

    login_view = import_string(package + '.views.oauth2_login')
    callback_view = import_string(package + '.views.oauth2_callback')

    urlpatterns = [
        url('^login/$', login_view,
            name=provider.id + '_login'),
        url('^login/callback/$', callback_view,
            name=provider.id + '_callback'),
    ]

    try:
        logout_view = import_string(provider.package + '.views.oauth2_logout')
    except ImportError:
        logout_view = None

    if logout_view is not None:
        urlpatterns += [
            url('^logout/$', logout_view,
                name=provider.id + '_logout'),
        ]

    return [url('^' + provider.get_slug() + '/', include(urlpatterns))]
