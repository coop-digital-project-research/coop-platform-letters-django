from django.contrib import admin

from .models import (
    Writer, Reader, WriterReaderSelection, WriterReaderAllocation
)


class ReadonlyFieldsOnChangeMixin():
    def get_readonly_fields(self, request, obj):
        readonly_fields = list(super(
            ReadonlyFieldsOnChangeMixin, self
        ).get_readonly_fields(request, obj))

        if obj:  # make uuid readonly if the model is already in DB
            readonly_fields.extend(self.readonly_fields_on_change)

        return tuple(readonly_fields)


@admin.register(Writer)
class WriterAdmin(ReadonlyFieldsOnChangeMixin, admin.ModelAdmin):
    list_display = (
        'first_name',
        'age',
        'uuid',
        'training_complete',
        'edit_url',
        'training_url',
        'profile_approved',
        'available_to_pick',
        'num_allocations',
        'updated_at',
    )

    list_filter = (
        'training_complete',
        'profile_approved',
        'available_to_pick',
        'updated_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    readonly_fields_on_change = ['uuid']

    def edit_url(self, instance):
        return '<a href="{}">[update]</a>'.format(
            instance.make_authenticated_writer_profile_url()
        )

    edit_url.allow_tags = True

    def training_url(self, instance):
        return '<a href="{}">[training]</a>'.format(
            instance.make_authenticated_training_url()
        )

    training_url.allow_tags = True

    def num_allocations(self, instance):
        return instance.allocations.count()


@admin.register(Reader)
class ReaderAdmin(ReadonlyFieldsOnChangeMixin, admin.ModelAdmin):
    list_display = (
        'first_name',
        'uuid',
        'got_postal_address',
        'prefer_forward_via_co_op',
        'choose_writers',
        'pre_letter_survey',
    )

    list_filter = (
        'got_postal_address',
        'prefer_forward_via_co_op',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    readonly_fields_on_change = ['uuid']

    def choose_writers(self, instance):
        return '<a href="{}">[choose writers]</a>'.format(
            instance.make_authenticated_choose_writers_url()
        )

    choose_writers.allow_tags = True

    def pre_letter_survey(self, instance):
        return '<a href="{}">[pre-survey]</a>'.format(
            instance.make_authenticated_pre_letter_survey_url()
        )

    pre_letter_survey.allow_tags = True


@admin.register(WriterReaderSelection)
class WriterReaderSelectionAdmin(admin.ModelAdmin):
    list_display = (
        'reader',
        'writer',
    )


@admin.register(WriterReaderAllocation)
class WriterReaderAllocationAdmin(ReadonlyFieldsOnChangeMixin,
                                  admin.ModelAdmin):
    list_display = (
        'reference',
        'allocated_at',
        'allocated_by',
        'writer',
        'reader',
        'letter_sent',
        'letter_received',
    )

    list_filter = (
        'allocated_at',
        'letter_sent',
        'letter_received',
    )

    readonly_fields_on_change = (
        'reference',
        'allocated_by',
        'writer',
        'reader',
    )
