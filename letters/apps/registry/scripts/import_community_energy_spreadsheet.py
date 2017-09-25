# Run me with:
# $ ./manage.py runscript import_community_energy_spreadsheet --script-args --traceback <filename.csv>  # noqa

import csv
import io
import re
import sys

from pprint import pprint
from collections import OrderedDict

from django.utils.text import slugify

from letters.apps.registry.models import CommunityEnergyGroup


def run(*args):
    if not len(args):
        raise RuntimeError("Please provide the filename of the CSV")

    csv_filename = args[0]
    with io.open(csv_filename, 'r') as f:
        non_empty_rows = filter(is_csv_row_valid, csv.DictReader(f))

        cleaned_rows = map(parse_row, non_empty_rows)

        for row in filter(filter_row, cleaned_rows):
            create_if_doesnt_exist(row)


def is_csv_row_valid(row):
    return 'Who' in row.keys()


def parse_row(row):
    name = normalize_string(row['Who'])
    slug = make_slug(name)

    phone = normalize_phone(normalize_string(row['Contact telephone']))

    return OrderedDict([
        ('name', name),
        ('slug', slug),
        ('legal_name', normalize_string(row['Registered Name'])),
        ('postcode', normalize_string(row['Postcode'])),
        ('website', normalize_string(row['Website'])),
        ('contact_telephone', phone),
        ('contact_email', normalize_string(row['Contact email'])),
        ('postcode_source_url', normalize_string(row['Source Postcode'])),
        ('group_source_url', normalize_string(row['Source organisation'])),
        ('_active', row.get('Active?', '').lower() == 'yes'),
        ('_type', normalize_string(row.get('Type', '').lower())),
    ])


def make_slug(name):
    return slugify(name)


def normalize_string(value):
    if value == '':
        return None
    else:
        return value.strip()


def normalize_phone(phone):
    if phone and phone.startswith('0'):
        return '+44' + re.sub('[^0-9+]', '', phone[1:])

    return phone


def filter_row(row):
    if row is None:
        return

    if not row['name']:
        # print("Filtering row without `Who` field: {}".format(row))
        return False

    if row['_type'] not in set(['renewable energy cic',
                                'renewable energy co-op',
                                'renewable energy bencom']):
        sys.stderr.write(
            "Dropping row with unknown type `{}`: {}\n".format(
                row['_type'], row['name'])
        )
        return False

    if not row['_active']:
        sys.stderr.write(
            "Dropping inactive organisation: {}\n".format(row['name'])
        )
        return False

    return True


def create_if_doesnt_exist(row):
    pprint(row)
    row.pop('_active')
    row.pop('_type')

    CommunityEnergyGroup.objects.get_or_create(
        name=row['name'],
        defaults=row
    )
