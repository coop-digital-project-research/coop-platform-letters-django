import luhn
import random


def generate_reference():
    """
    Return a luhn-valid 10-digit reference like:
    123-456  (where 6 is the check digit)
    """
    from . import WriterReaderAllocation

    characters = '0123456789'

    for attempt in range(10):
        five_digits = ''.join(random.choice(characters) for _ in range(5))
        reference = '{}-{}{}'.format(
            five_digits[0:3],
            five_digits[3:5],
            luhn.generate(five_digits))

        try:
            WriterReaderAllocation.objects.get(reference=reference)
        except WriterReaderAllocation.DoesNotExist:
            return reference

    raise RuntimeError('Failed repeatedly to generate a unique reference.')
