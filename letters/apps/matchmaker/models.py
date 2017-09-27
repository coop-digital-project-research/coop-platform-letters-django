import datetime
import uuid

import jwt

from django.conf import settings
from django.db import models
from django.urls import reverse


class Sender(models.Model):

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4
    )

    first_name = models.CharField(
        max_length=128,
        help_text="We only ask for your first name so that your identity is protected."
    )

    private_story = models.TextField(blank=True)

    profile_story = models.TextField(
        blank=True,
        help_text="A short summary will help people who need support find a letter writer they can relate to."
    )

    age = models.IntegerField(
        blank=True,
        null=True,
        help_text="This will help people who want to receive a letter make a decision about who writes to them."
    )

    def make_json_web_token(self):
        data = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'sender_uuid': str(self.uuid),
        }

        result = jwt.encode(data, settings.SECRET_KEY)
        return result

    def make_authenticated_sender_profile_url(self):
        return reverse(
            'update-sender-profile',
            kwargs={'json_web_token': self.make_json_web_token()}
        )
