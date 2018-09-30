from django.conf.urls import patterns, url, include
from django.utils.module_loading import import_string


def default_urlpatterns(provider):
    urlpatterns = patterns(provider.package + '.views',
                           url('^login/$', 'oauth2_login',
                               name=provider.id + "_login"),
                           url('^login/callback/$', 'oauth2_callback',
                               name=provider.id + "_callback"))

    try:
        logout_view = import_string(provider.package + '.views.oauth2_logout')
    except ImportError:
        logout_view = None

    if logout_view is not None:
        urlpatterns += [
            url('^logout/$', logout_view,
                name=provider.id + '_logout'),
        ]

    return patterns('', url('^' + provider.id + '/', include(urlpatterns)))
