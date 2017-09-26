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
        max_length=128
    )

    profile_story = models.TextField()

    age = models.IntegerField()

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
