import datetime
import uuid

import jwt

from django.conf import settings
from django.db import models
from django.urls import reverse


class Reader(models.Model):
    class Meta:
        ordering = ('-created_at',)

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    first_name = models.CharField(
        max_length=128,
        default=""
    )

    got_postal_address = models.BooleanField(
        default=False
    )

    prefer_forward_via_co_op = models.NullBooleanField(
        default=None
    )

    baseline_survey_complete = models.BooleanField(
        default=False
    )

    get_started_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    chase_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    baseline_survey_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    invite_to_pick_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    priming_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    follow_up_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    def __str__(self):
        return '{} ({})'.format(self.uuid, self.first_name)

    def make_json_web_token(self):
        data = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'reader_uuid': str(self.uuid),
        }

        result = jwt.encode(data, settings.SECRET_KEY)
        return result

    def make_authenticated_choose_writers_url(self):
        return reverse(
            'reader-choose-writers',
            kwargs={'json_web_token': self.make_json_web_token()}
        )

    def make_authenticated_pre_letter_survey_url(self):
        return reverse(
            'reader-pre-letter-survey',
            kwargs={'json_web_token': self.make_json_web_token()}
        )

    @property
    def selected_writers(self):
        return (s.writer for s in self.selections.all())
