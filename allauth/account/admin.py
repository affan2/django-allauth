from django.contrib import admin

from . import app_settings
from .adapter import get_adapter
from .models import EmailAddress, EmailConfirmation
from .forms import EmailAddressAdminForm


class EmailAddressAdmin(admin.ModelAdmin):
    model = EmailAddress
    form = EmailAddressAdminForm
    list_display = ('email', 'user', 'primary', 'verified')
    list_filter = ('primary', 'verified')
    search_fields = []
    raw_id_fields = ('user',)
    autocomplete_fields = ['user']

    def get_search_fields(self, request):
        base_fields = get_adapter(request).get_user_search_fields()
        return ['email'] + list(['user__' + a for a in base_fields])


class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'created', 'sent', 'key')
    list_filter = ('sent',)
    raw_id_fields = ('email_address',)


if not app_settings.EMAIL_CONFIRMATION_HMAC:
    admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
