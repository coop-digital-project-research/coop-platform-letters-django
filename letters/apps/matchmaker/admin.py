from django.contrib import admin

from .models import Sender


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'uuid',
        'edit_url',
    )

    def edit_url(self, instance):
        return '<a href="{}">[Link to update page]</a>'.format(
            instance.make_authenticated_sender_profile_url()
        )

    edit_url.allow_tags = True
