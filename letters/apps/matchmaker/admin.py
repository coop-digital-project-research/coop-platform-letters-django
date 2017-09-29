from django.contrib import admin

from .models import Sender, Receiver, SenderReceiverPairing


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


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'choose_senders',
    )

    def choose_senders(self, instance):
        return '<a href="{}">[Link to choose senders]</a>'.format(
            instance.make_authenticated_choose_senders_url()
        )

    choose_senders.allow_tags = True


@admin.register(SenderReceiverPairing)
class SenderReceiverPairingAdmin(admin.ModelAdmin):
    list_display = (
        'receiver',
        'sender',
    )
