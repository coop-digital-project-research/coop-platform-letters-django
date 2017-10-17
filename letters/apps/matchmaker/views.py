import datetime
import random

import jwt

from django.db.models import Q
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from django.urls import reverse
from django.utils import timezone


from .models import (
    Writer, Reader, WriterReaderSelection, WriterReaderAllocation
)
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
    uuid_key = 'sender_uuid'  # TODO: rename to writer_uuid


class GetReaderObjectFromJWTMixin(GetObjectFromJWT):
    object_class = Reader
    uuid_key = 'reader_uuid'


class UpdateWriterProfileView(GetWriterObjectFromJWTMixin, UpdateView):
    form_class = WriterForm
    template_name = 'matchmaker/update_writer_profile.html'
    model = Writer
    context_object_name = 'writer'

    def get(self, *args, **kwargs):
        writer = self.get_object()
        if writer.training_complete:
            return super(
                UpdateWriterProfileView, self
            ).get(*args, **kwargs)
        else:
            return redirect(
                reverse(
                    'writer-training',
                    kwargs={'json_web_token': self.kwargs['json_web_token']}
                )
            )

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

    def get(self, *args, **kwargs):
        reader = self.get_object()

        if reader.selections.count() > 0:
            return redirect(
                reverse(
                    'reader-confirmation',
                    kwargs={'json_web_token': self.kwargs['json_web_token']}
                )
            )
        else:
            return super(ReaderChooseWritersView, self).get(*args, **kwargs)

    def post(self, request, **kwargs):
        reader = self.get_object()
        writer_uuids = request.POST.getlist('writers')

        self._clear_existing_writers(reader)
        self._create_pairings(
            reader,
            (Writer.objects.get(uuid=u) for u in writer_uuids)
        )

        return redirect(
            reverse(
                'reader-confirmation',
                kwargs={'json_web_token': self.kwargs['json_web_token']}
            )
        )

    def get_queryset(self):
        reader = self.get_object()
        random.seed(reader.uuid)

        writers = [ob for ob in Writer.objects.filter(available_to_pick=True)]

        random.shuffle(writers)
        return writers

    def get_context_data(self, **kwargs):
        existing_context = super(
            ReaderChooseWritersView, self
        ).get_context_data(**kwargs)

        existing_context.update(
            {'reader': self.get_object()}
        )
        return existing_context

    @staticmethod
    def _clear_existing_writers(for_reader):
        WriterReaderSelection.objects.filter(reader=for_reader).delete()

    @staticmethod
    def _create_pairings(reader, writers):
        for writer in writers:
            (pairing, created) = WriterReaderSelection.objects.get_or_create(
                writer=writer,
                reader=reader
            )


class ReaderConfirmationView(GetReaderObjectFromJWTMixin, DetailView):
    template_name = 'matchmaker/reader_confirmation.html'
    model = Reader
    context_object_name = 'reader'


class WriterGuideView(TemplateView):
    template_name = 'matchmaker/writer_guide.html'


class ReaderPreLetterSurveyView(GetReaderObjectFromJWTMixin, DetailView):
    template_name = 'matchmaker/reader_pre_letter_survey.html'
    model = Reader
    context_object_name = 'reader'


class AdminTaskListView(TemplateView):
    template_name = 'matchmaker/admin_task_list.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'allocations':
            self._writer_reader_allocations(),

            'writers_awaiting_get_started_email':
            self._writers_awaiting_get_started_email(),

            'writers_awaiting_chase_email':
            self._writers_awaiting_chase_email(),

            'writers_awaiting_final_chase_email':
            self._writers_awaiting_final_chase_email(),

            'readers_awaiting_baseline_survey_email':
            self._readers_awaiting_baseline_survey_email(),

            'readers_awaiting_get_started_email':
            self._readers_awaiting_get_started_email(),

            'readers_awaiting_chase_email':
            self._readers_awaiting_chase_email(),

            'readers_without_postal_options':
            self._readers_without_postal_options(),

            'readers_awaiting_invite_to_pick_email':
            self._readers_awaiting_invite_to_pick_email(),

            'allocations_awaiting_writer_priming_email':
            self.allocations_awaiting_writer_priming_email(),

            'allocations_awaiting_reader_priming_email':
            self.allocations_awaiting_reader_priming_email(),

            'allocations_awaiting_writer_follow_up_email':
            self.allocations_awaiting_writer_follow_up_email(),

            'allocations_awaiting_reader_follow_up_email':
            self.allocations_awaiting_reader_follow_up_email(),
        }
        return context

    def _writer_reader_allocations(self):
        return WriterReaderAllocation.objects.all()

    def _writers_awaiting_get_started_email(self):
        return Writer.objects.filter(
            get_started_email_sent=None
        )

    def _writers_awaiting_chase_email(self):
        two_days_ago = timezone.now() - datetime.timedelta(days=2)

        return Writer.objects.filter(
            chase_email_sent=None,
            age=None,
            get_started_email_sent__lt=two_days_ago,
        ).order_by('get_started_email_sent')

    def _writers_awaiting_final_chase_email(self):
        three_days_ago = timezone.now() - datetime.timedelta(days=3)

        return Writer.objects.filter(
            final_chase_email_sent=None,
            age=None,
            chase_email_sent__lt=three_days_ago,
        ).order_by('chase_email_sent')

    def _readers_awaiting_baseline_survey_email(self):
        return Reader.objects.filter(
            baseline_survey_email_sent=None,
            got_postal_address=True,
            prefer_forward_via_co_op__isnull=False,
        )

    def _readers_awaiting_get_started_email(self):
        return Reader.objects.filter(
            get_started_email_sent=None
        )

    def _readers_awaiting_chase_email(self):
        two_days_ago = timezone.now() - datetime.timedelta(days=2)

        return Reader.objects.filter(
            chase_email_sent=None,
            got_postal_address=False,
            prefer_forward_via_co_op=None,
            get_started_email_sent__lt=two_days_ago,
        ).order_by('get_started_email_sent')

    def _readers_without_postal_options(self):
        return Reader.objects.filter(
            Q(got_postal_address=False) | Q(prefer_forward_via_co_op=None),
            get_started_email_sent__isnull=False,
        )

    def _readers_awaiting_invite_to_pick_email(self):
        one_day_ago = timezone.now() - datetime.timedelta(days=1)

        return Reader.objects.filter(
            invite_to_pick_email_sent=None,
            got_postal_address=True,
            prefer_forward_via_co_op__isnull=False,
            baseline_survey_email_sent__lt=one_day_ago,
        )

    def allocations_awaiting_reader_priming_email(self):
        return WriterReaderAllocation.objects.filter(
            reader_priming_email_sent=None,
        )

    def allocations_awaiting_writer_priming_email(self):
        return WriterReaderAllocation.objects.filter(
            writer_priming_email_sent=None,
        )

    def allocations_awaiting_reader_follow_up_email(self):
        ten_days_ago = timezone.now() - datetime.timedelta(days=10)

        return WriterReaderAllocation.objects.filter(
            reader_follow_up_email_sent=None,
            reader_priming_email_sent__isnull=False,
            reader_priming_email_sent__lt=ten_days_ago,
        )

    def allocations_awaiting_writer_follow_up_email(self):
        ten_days_ago = timezone.now() - datetime.timedelta(days=10)

        return WriterReaderAllocation.objects.filter(
            writer_follow_up_email_sent=None,
            writer_priming_email_sent__isnull=False,
            writer_priming_email_sent__lt=ten_days_ago,
        )


class AdminTaskListWriterEmailView(DetailView):
    model = Writer
    context_object_name = 'writer'

    def get_template_names(self, *args, **kwargs):
        email_slug = self.kwargs['email_slug']
        return 'matchmaker/writer_emails/{}.html'.format(
            email_slug.replace('-', '_')
        )


class AdminTaskListReaderEmailView(DetailView):
    model = Reader
    context_object_name = 'reader'

    def get_template_names(self, *args, **kwargs):
        email_slug = self.kwargs['email_slug']
        return 'matchmaker/reader_emails/{}.html'.format(
            email_slug.replace('-', '_')
        )


class AdminTaskListAllocationEmailView(DetailView):
    model = WriterReaderAllocation
    context_object_name = 'allocation'

    def get_template_names(self, *args, **kwargs):
        email_slug = self.kwargs['email_slug']

        return 'matchmaker/allocation_emails/{}.html'.format(
            email_slug.replace('-', '_')
        )
