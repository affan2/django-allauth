from allauth.socialaccount.tests import create_oauth2_tests
from allauth.tests import MockedResponse
from allauth.socialaccount.providers import registry

from .provider import BIMobjectProvider


class BIMobjectTests(create_oauth2_tests(registry.by_id(BIMobjectProvider.id))):
    def get_mocked_response(self):
        return MockedResponse(200, """
        {
            "user_id": "b61c6f52-0785-434c-a412-f3bb824a21064",
            "name": "Jane Doe",
            "given_name": "Jane",
            "family_name": "Doe",
            "email": "janedoe@bimobject.com"
        }
        """)
