import datetime
import uuid

import jwt

from django.conf import settings
from django.db import models
from django.urls import reverse


class Writer(models.Model):
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
        help_text=(
            "We only ask for your first name so that your identity is "
            "protected."
        )
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
        help_text=(
            "A short summary will help people who need support find a letter "
            "writer they can relate to."
        )
    )

    age = models.IntegerField(
        blank=True,
        null=True,
        help_text=(
            "This will help people who want to receive a letter make a "
            "decision about who writes to them."
        )
    )

    training_complete = models.BooleanField(
        default=False,
    )

    profile_approved = models.BooleanField(
        default=False,
        help_text=(
            "This indicates that we've approved the content of a profile. "
            "See also `available_to_pick`"
        )
    )

    available_to_pick = models.BooleanField(
        default=False,
        help_text=(
            "This controls whether this writer is visible for readers to "
            "to pick. We set it when we first approve a profile and unset it "
            "when we allocate them to reader. If they want to write another "
            "letter we could set it again."
        )
    )

    get_started_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    chase_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    final_chase_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    def __str__(self):
        return '{} ({})'.format(self.uuid, self.first_name)

    def make_json_web_token(self):
        data = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'writer_uuid': str(self.uuid),
            'sender_uuid': str(self.uuid),
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
