import uuid

from django.db import models


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
