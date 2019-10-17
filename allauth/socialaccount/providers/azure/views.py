from __future__ import unicode_literals

import requests

from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import AzureProvider


LOGIN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0'
GRAPH_URL = 'https://graph.microsoft.com/v1.0'


class AzureOAuth2Adapter(OAuth2Adapter):
    """
    Docs available at:
    https://docs.microsoft.com/en-us/azure/active-directory/develop/active-directory-v2-protocols
    """
    provider_id = AzureProvider.id
    access_token_url = LOGIN_URL + '/token'
    authorize_url = LOGIN_URL + '/authorize'
    profile_url = 'https://graph.microsoft.com/v1.0/me'
    # Can be used later to obtain group data. Needs 'Group.Read.All' or
    # similar.
    #
    # See https://developer.microsoft.com/en-us/graph/docs/api-reference/beta/api/user_list_memberof  # noqa
    groups_url = GRAPH_URL + '/me/memberOf?$select=displayName'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        extra_data = {}

        resp = requests.get(self.profile_url, headers=headers)

# See:
#
# https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_get  # noqa
#
# example of what's returned (in python format)
#
# {'displayName':'John Smith','mobilePhone': None,
# 'preferredLanguage':'en-US','jobTitle':'Director',
# 'userPrincipalName':'john@smith.com',
# '@odata.context':
# 'https://graph.microsoft.com/v1.0/$metadata#users/$entity',
# 'officeLocation':'Paris','businessPhones': [],
# 'mail':'john@smith.com','surname':'Smith',
# 'givenName':'John','id':'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'}

        profile_data = resp.json()
        extra_data.update(profile_data)

        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)


oauth2_login = OAuth2LoginView.adapter_view(AzureOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AzureOAuth2Adapter)
