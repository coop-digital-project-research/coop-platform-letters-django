from django.contrib import admin

from .models import Sender, Receiver, SenderReceiverPairing


@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'age',
        'uuid',
        'training_complete',
        'edit_url',
        'training_url',
    )

    readonly_fields = (
        'uuid',
    )

    def edit_url(self, instance):
        return '<a href="{}">[Link to update page]</a>'.format(
            instance.make_authenticated_sender_profile_url()
        )

    edit_url.allow_tags = True

    def training_url(self, instance):
        return '<a href="{}">[Link to training]</a>'.format(
            instance.make_authenticated_training_url()
        )

    training_url.allow_tags = True


@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'choose_senders',
        'pre_letter_survey'
    )

    def choose_senders(self, instance):
        return '<a href="{}">[Link to choose senders]</a>'.format(
            instance.make_authenticated_choose_senders_url()
        )

    choose_senders.allow_tags = True

    def pre_letter_survey(self, instance):
        return '<a href="{}">[Link to pre-survey]</a>'.format(
            instance.make_authenticated_pre_letter_survey_url()
        )

    pre_letter_survey.allow_tags = True


@admin.register(SenderReceiverPairing)
class SenderReceiverPairingAdmin(admin.ModelAdmin):
    list_display = (
        'receiver',
        'sender',
    )
