from django.contrib import admin

from .models import Sender


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'age',
        'uuid',
        'edit_url',
    )

    readonly_fields = (
        'uuid',
    )

    def edit_url(self, instance):
        return '<a href="{}">[Link to update page]</a>'.format(
            instance.make_authenticated_sender_profile_url()
        )

    edit_url.allow_tags = True
