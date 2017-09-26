from django.contrib import admin

from .models import Sender


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'uuid',
        'make_authenticated_sender_profile_url',
    )
