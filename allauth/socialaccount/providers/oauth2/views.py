from __future__ import absolute_import

from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from allauth.utils import build_absolute_uri, get_request_param
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import get_next_redirect_url
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount import providers
from allauth.socialaccount.providers.oauth2.client import (OAuth2Client,
                                                           OAuth2Error)
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialToken, SocialLogin
from ..base import AuthAction, AuthError


class OAuth2Adapter(object):
    expires_in_key = 'expires_in'
    supports_state = True
    redirect_uri_protocol = None  # None: use ACCOUNT_DEFAULT_HTTP_PROTOCOL
    access_token_method = 'POST'
    login_cancelled_error = 'access_denied'

    def get_provider(self):
        return providers.registry.by_id(self.provider_id)

    def complete_login(self, request, app, access_token, **kwargs):
        """
        Returns a SocialLogin instance
        """
        raise NotImplementedError

    def parse_token(self, data):
        token = SocialToken(token=data['access_token'])
        token.token_secret = data.get('refresh_token', '')
        expires_in = data.get(self.expires_in_key, None)
        if expires_in:
            token.expires_at = timezone.now() + timedelta(
                seconds=int(expires_in))
        return token


class OAuth2View(object):
    @classmethod
    def adapter_view(cls, adapter):
        def view(request, *args, **kwargs):
            self = cls()
            self.request = request
            self.adapter = adapter()
            return self.dispatch(request, *args, **kwargs)
        return view

    def get_client(self, request, app):
        callback_url = reverse(self.adapter.provider_id + "_callback")
        logout_url = reverse(self.adapter.provider_id + "_logout")
        protocol = (self.adapter.redirect_uri_protocol
                    or app_settings.DEFAULT_HTTP_PROTOCOL)
        callback_url = build_absolute_uri(
            request, callback_url,
            protocol=protocol)
        logout_url = build_absolute_uri(
            request, logout_url,
            protocol=protocol)
        provider = self.adapter.get_provider()
        scope = provider.get_scope(request)
        client = OAuth2Client(self.request, app.client_id, app.secret,
                              self.adapter.access_token_method,
                              self.adapter.access_token_url,
                              callback_url,
                              logout_url,
                              scope)
        return client


class OAuth2LoginView(OAuth2View):
    def dispatch(self, request):
        provider = self.adapter.get_provider()
        app = provider.get_app(self.request)
        client = self.get_client(request, app)
        action = request.GET.get('action', AuthAction.AUTHENTICATE)
        auth_url = self.adapter.authorize_url
        auth_params = provider.get_auth_params(request, action)
        client.state = SocialLogin.stash_state(request)
        try:
            return HttpResponseRedirect(client.get_redirect_url(
                auth_url, auth_params))
        except OAuth2Error as e:
            return render_authentication_error(
                request,
                provider.id,
                exception=e)


class OAuth2CallbackView(OAuth2View):
    def dispatch(self, request):
        if 'error' in request.GET or 'code' not in request.GET:
            # Distinguish cancel from error
            auth_error = request.GET.get('error', None)
            if auth_error == self.adapter.login_cancelled_error:
                error = AuthError.CANCELLED
            else:
                error = AuthError.UNKNOWN
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                error=error)
        app = self.adapter.get_provider().get_app(self.request)
        client = self.get_client(request, app)

        request.session['last_sociallogin'] = self.adapter.provider_id

        try:
            access_token = client.get_access_token(request.GET['code'])
            token = self.adapter.parse_token(access_token)
            token.app = app
            login = self.adapter.complete_login(request,
                                                app,
                                                token,
                                                response=access_token)
            login.token = token
            if self.adapter.supports_state:
                login.state = SocialLogin \
                    .verify_and_unstash_state(
                        request,
                        get_request_param(request, 'state'))
            else:
                login.state = SocialLogin.unstash_state(request)
            return complete_social_login(request, login)
        except (PermissionDenied, OAuth2Error) as e:
            return render_authentication_error(
                request,
                self.adapter.provider_id,
                exception=e)


class OAuth2LogoutView(OAuth2View):
    def dispatch(self, request, next_page=None):
        """
        Redirects to the social logout page.
        next_page is used to let the server send back the user. If empty,
        the redirect url is built on request data.
        """
        if request.method != "POST":
            return HttpResponseRedirect("/")

        redirect_url = next_page or self.get_redirect_url()
        redirect_to = request.build_absolute_uri(redirect_url)

        app = self.adapter.get_provider().get_app(request)
        client = self.get_client(request, app)

        return HttpResponseRedirect(client.get_logout_url(redirect_to))

    def get_redirect_url(self):
        """
        Returns the url to redirect after logout.
        """
        request = self.request
        return (
            get_next_redirect_url(request) or
            get_adapter(request).get_logout_redirect_url(request)
        )


