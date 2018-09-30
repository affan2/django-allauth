import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)

from .provider import BIMobjectProvider


class BIMobjectOAuth2Adapter(OAuth2Adapter):
    provider_id = BIMobjectProvider.id
    supports_state = False

    @property
    def authorize_url(self):
        path = 'identity/connect/authorize'
        return '{0}/{1}'.format(self._get_endpoint(), path)

    @property
    def access_token_url(self):
        path = "identity/connect/token"
        return '{0}/{1}'.format(self._get_endpoint(), path)

    @property
    def profile_url(self):
        path = 'identity/connect/userinfo'
        return '{0}/{1}'.format(self._get_endpoint(), path)

    @property
    def logout_url(self):
        path = 'identity/connect/endsession'
        return '{0}/{1}'.format(self._get_endpoint(), path)

    def _get_endpoint(self):
        settings = self.get_provider().get_settings()
        if settings.get('MODE') == 'live':
            return 'https://accounts.bimobject.com'
        elif settings.get('MODE') == 'staging':
            return 'http://accounts-staging.ad.bimobject.com'
        else:
            return 'http://accounts-portaldev.ad.bimobject.com'

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer ' + token.token}
        response = requests.get(
            self.profile_url,
            params={'schema': 'openid'},
            headers=headers
        )
        extra_data = response.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(BIMobjectOAuth2Adapter)
oauth2_logout = OAuth2LogoutView.adapter_view(BIMobjectOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(BIMobjectOAuth2Adapter)
