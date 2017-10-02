from django.contrib import admin

from .models import Writer, Reader, WriterReaderPairing


@admin.register(Writer)
class WriterAdmin(admin.ModelAdmin):
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
            instance.make_authenticated_writer_profile_url()
        )

    edit_url.allow_tags = True

    def training_url(self, instance):
        return '<a href="{}">[Link to training]</a>'.format(
            instance.make_authenticated_training_url()
        )

    training_url.allow_tags = True


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = (
        'uuid',
        'choose_writers',
    )

    def choose_writers(self, instance):
        return '<a href="{}">[Link to choose writers]</a>'.format(
            instance.make_authenticated_choose_writers_url()
        )

    choose_writers.allow_tags = True


@admin.register(WriterReaderPairing)
class WriterReaderPairingAdmin(admin.ModelAdmin):
    list_display = (
        'reader',
        'writer',
    )
