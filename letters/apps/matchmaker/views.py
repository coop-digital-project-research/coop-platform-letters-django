import jwt

from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse


from .models import Writer, Reader, WriterReaderPairing
from .forms import WriterForm


class GetObjectFromJWT:

    def get_object(self, *args, **kwargs):
        json_web_token = self.kwargs['json_web_token']

        try:
            result = jwt.decode(json_web_token, settings.SECRET_KEY)

        except jwt.exceptions.ExpiredSignatureError:
            # TODO: handle this
            raise

        except jwt.exceptions.InvalidTokenError:
            # TODO: handle more general types of token error
            # https://github.com/jpadilla/pyjwt/blob/master/jwt/exceptions.py
            raise

        return self.object_class.objects.get(uuid=result[self.uuid_key])


class GetWriterObjectFromJWTMixin(GetObjectFromJWT):
    object_class = Writer
    uuid_key = 'writer_uuid'


class GetReaderObjectFromJWTMixin(GetObjectFromJWT):
    object_class = Reader
    uuid_key = 'reader_uuid'


class UpdateWriterProfileView(GetWriterObjectFromJWTMixin, UpdateView):
    form_class = WriterForm
    template_name = 'matchmaker/update_writer_profile.html'
    model = Writer
    context_object_name = 'writer'

    def get_success_url(self, **kwargs):
        return reverse(
            'writer-profile-detail',
            kwargs={'json_web_token': self.kwargs['json_web_token']}
        )


class WriterProfileDetailView(GetWriterObjectFromJWTMixin, DetailView):
    template_name = 'matchmaker/writer_profile.html'
    model = Writer
    context_object_name = 'writer'

    def get_context_data(self, **kwargs):
        existing_context = super(
            WriterProfileDetailView, self
        ).get_context_data(**kwargs)

        existing_context.update(
            {'json_web_token': self.kwargs['json_web_token']}
        )
        return existing_context


class WriterTrainingView(GetWriterObjectFromJWTMixin, TemplateView):
    template_name = 'matchmaker/writer_training.html'

    def post(self, request, **kwargs):
        writer = self.get_object()
        writer.training_complete = True
        writer.save()

        return redirect(
            reverse(
                'update-writer-profile',
                kwargs={'json_web_token': self.kwargs['json_web_token']}
            )
        )


class ReaderChooseWritersView(GetReaderObjectFromJWTMixin, ListView):
    template_name = 'matchmaker/reader_choose_writers.html'
    model = Writer
    context_object_name = 'writers'

    def post(self, request, **kwargs):
        reader = self.get_object()
        writer_uuids = request.POST.getlist('writers')

        self._clear_existing_writers(reader)
        self._create_pairings(
            reader,
            (Writer.objects.get(uuid=u) for u in writer_uuids)
        )

        return redirect(
            reverse('reader-confirmation')
        )

    @staticmethod
    def _clear_existing_writers(for_reader):
        WriterReaderPairing.objects.filter(reader=for_reader).delete()

    @staticmethod
    def _create_pairings(reader, writers):
        for writer in writers:
            (pairing, created) = WriterReaderPairing.objects.get_or_create(
                writer=writer,
                reader=reader
            )


class ReaderConfirmationView(TemplateView):
    template_name = 'matchmaker/reader_confirmation.html'


class SenderGuideView(TemplateView):
    template_name = 'matchmaker/sender_guide.html'
