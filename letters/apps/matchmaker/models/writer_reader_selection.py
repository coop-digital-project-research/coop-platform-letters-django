from django.db import models

from .writer import Writer
from .reader import Reader


class WriterReaderSelection(models.Model):
    """
    Indicates that the given reader is happy to receive a letter from the given
    writer.

    This doesn't mean that writer will necessarily be allocated to that reader.
    """

    class Meta:
        unique_together = (('writer', 'reader'))

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    writer = models.ForeignKey(Writer)
    reader = models.ForeignKey(Reader, related_name='selections')

    def __str__(self):
        return '{} --> {}'.format(self.reader, self.writer)
