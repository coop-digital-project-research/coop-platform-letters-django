from django.test import TestCase
from . import PostcodeLookUp

class TestPostcodeLookUp(TestCase):
    def test_that_the_postcode_lookup_returns_correct_values_for_a_postcode_matching_file_format(self):
        got = PostcodeLookUp.look_up("CM3 3AJ")
        self.assertAlmostEqual(got[0], 51.76953719999999, places = 3)
        self.assertAlmostEqual(got[1], 0.5639039999999795, places = 3)

    def test_that_the_postcode_lookup_returns_correct_values_for_a_postcode_with_no_spaces(self):
        got = PostcodeLookUp.look_up("CM33AJ")
        self.assertAlmostEqual(got[0], 51.76953719999999, places = 3)
        self.assertAlmostEqual(got[1], 0.5639039999999795, places = 3)

    def test_that_the_postcode_lookup_returns_correct_values_for_a_postcode_with_extra_spaces(self):
        got = PostcodeLookUp.look_up(" CM33AJ  ")
        self.assertAlmostEqual(got[0], 51.76953719999999, places = 3)
        self.assertAlmostEqual(got[1], 0.5639039999999795, places = 3)

    def test_that_the_postcode_lookup_returns_correct_values_for_a_postcode_regardless_of_case(self):
        got = PostcodeLookUp.look_up("cM3 3aj")
        self.assertAlmostEqual(got[0], 51.76953719999999, places = 3)
        self.assertAlmostEqual(got[1], 0.5639039999999795, places = 3)

    def test_that_the_postcode_lookup_raises_for_not_found_postcodes(self):
        self.assertRaises(
            PostcodeLookUp.PostcodeNotFoundOrInvalid,
            lambda: PostcodeLookUp.look_up("FOOBAR")
        )

    def test_that_the_postcode_lookup_returns_correct_values_for_manchester_postcode(self):
        got = PostcodeLookUp.look_up("M4 2AH")
        self.assertAlmostEqual(got[0], 53.4863, places = 3)
        self.assertAlmostEqual(got[1], -2.2397, places = 3)

    def test_that_the_postcode_lookup_doesnt_accepted_int(self):
        self.assertRaises(TypeError, lambda: PostcodeLookUp.look_up(1))

    def test_that_the_postcode_lookup_doesnt_accepted_none(self):
        self.assertRaises(TypeError, lambda: PostcodeLookUp.look_up())
