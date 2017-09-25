import csv
import gzip
import os
import re
from bng_to_latlon import OSGB36toWGS84


DIRECTORY = os.path.abspath(os.path.dirname(__file__))
POSTCODE_FILENAME = os.path.join(DIRECTORY, "all_postcodes.csv.gz")


class PostcodeLookUp():
    class PostcodeNotFoundOrInvalid(ValueError):
        pass

    @staticmethod
    def look_up(postcode):
        if not isinstance(postcode, str):
            raise TypeError('Postcode should be a string, got {}'.format(postcode))

        with gzip.open(POSTCODE_FILENAME, 'rt') as f:
            for row in csv.reader(f):
                easting = int(row[2])
                northing = int(row[3])
                if (PostcodeLookUp._normalise(row[0])
                    == PostcodeLookUp._normalise(postcode)):
                    return OSGB36toWGS84(easting, northing)

        raise PostcodeLookUp.PostcodeNotFoundOrInvalid()

    @staticmethod
    def _normalise(postcode):
        return re.sub('[^A-Z0-9]', '', postcode.upper())
