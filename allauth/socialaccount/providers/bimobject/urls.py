from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import BIMobjectProvider

urlpatterns = default_urlpatterns(BIMobjectProvider)
