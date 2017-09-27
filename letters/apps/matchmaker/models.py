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

    profile_story = models.TextField(
        help_text="Write a couple of sentences to help readers understand how you got into debt. This will help them pick somebody they can relate to."
    )

    age = models.IntegerField(
        help_text="This will help people who want to receive a letter make a decision about who writes to them."
    )

    def make_json_web_token(self):
        data = {
            'sender_uuid': str(self.uuid),
        }

        result = jwt.encode(data, settings.SECRET_KEY)
        return result

    def make_authenticated_sender_profile_url(self):
        return reverse(
            'update-sender-profile',
            kwargs={'json_web_token': self.make_json_web_token()}
        )
