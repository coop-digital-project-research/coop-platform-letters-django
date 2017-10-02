import datetime
import uuid

import jwt

from django.conf import settings
from django.db import models
from django.urls import reverse


class Writer(models.Model):

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    first_name = models.CharField(
        max_length=128,
        help_text="We only ask for your first name so that your identity is protected."
    )

    private_story = models.TextField(
        blank=True,
        help_text=(
            "This is what you told us about your debt situation - we're "
            "showing it to you here to help you write a couple of sentences "
            "about how you got into debt."
        )
    )

    profile_story = models.TextField(
        blank=True,
        help_text="A short summary will help people who need support find a letter writer they can relate to."
    )

    age = models.IntegerField(
        blank=True,
        null=True,
        help_text="This will help people who want to receive a letter make a decision about who writes to them."
    )

    training_complete = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return '{} {}'.format(self.first_name, self.uuid)

    def make_json_web_token(self):
        data = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'writer_uuid': str(self.uuid),
        }

        result = jwt.encode(data, settings.SECRET_KEY)
        return result

    def make_authenticated_writer_profile_url(self):
        return reverse(
            'update-writer-profile',
            kwargs={'json_web_token': self.make_json_web_token()}
        )

    def make_authenticated_training_url(self):
        return reverse(
            'writer-training',
            kwargs={'json_web_token': self.make_json_web_token()}
        )


class Reader(models.Model):

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    def __str__(self):
        return str(self.uuid)

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


class WriterReaderPairing(models.Model):

    class Meta:
        unique_together = (('writer', 'reader'))

    writer = models.ForeignKey(Writer)
    reader = models.ForeignKey(Reader)

    def __str__(self):
        return '{} --> {}'.format(self.reader, self.writer)
