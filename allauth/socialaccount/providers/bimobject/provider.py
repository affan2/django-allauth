from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class BIMobjectAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get('picture')

    def to_str(self):
        return self.account.extra_data.get('name',
                                           super(BIMobjectAccount, self).to_str())


class BIMobjectProvider(OAuth2Provider):
    id = 'bimobject'
    name = 'BIMobject'
    package = 'allauth.socialaccount.providers.bimobject'
    account_class = BIMobjectAccount

    def get_default_scope(self):
        return [
            'openid',
            'email',
            'profile',
            'address'
        ]

    def extract_uid(self, data):
        return str(data['sub'])

    def extract_common_fields(self, data):
        return dict(
            first_name=data.get('given_name', ''),
            last_name=data.get('family_name', ''),
            name=data.get('name', ''),
            email=data.get('email'),
            email_verified=data.get('email_verified'),
            picture=data.get('picture'),
            profile=data.get('profile'),
            occupation=data.get('occupation'),
            company=data.get('company'),
            locale=data.get('locale'),
        )


providers.registry.register(BIMobjectProvider)
