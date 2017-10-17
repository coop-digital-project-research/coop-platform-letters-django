from django.db import models
from django.contrib.auth.models import User

from .utils import generate_reference
from .writer import Writer
from .reader import Reader


class WriterReaderAllocation(models.Model):
    """
    Indicates a letter that's going to be written from a Writer to a Reader.
    """

    class Meta:
        ordering = ('-allocated_at',)
        unique_together = (('writer', 'reader'))

    reference = models.CharField(
        primary_key=True,
        null=False,
        max_length=7,  # e.g. '123-456'
        default=generate_reference,
        editable=False,
    )

    allocated_at = models.DateTimeField(auto_now_add=True, null=True)

    allocated_by = models.ForeignKey(User, null=True)

    writer = models.ForeignKey(Writer)

    reader = models.ForeignKey(Reader)

    letter_sent = models.NullBooleanField(default=None)

    letter_received = models.NullBooleanField(default=None)

    writer_priming_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    writer_follow_up_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    writer_midway_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    writer_sent_letter_closure_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    writer_no_sent_letter_closure_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    reader_priming_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    reader_follow_up_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    reader_got_letter_closure_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )

    reader_no_letter_closure_email_sent = models.DateField(
        blank=True, null=True,
        default=None
    )
