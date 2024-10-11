from django.test import TestCase

from app.models import ShortURL


class ShortURLModelTestCase(TestCase):
    def test_duplicate_short_key(self):
        ShortURL.objects.create(short_key="abc", url="http://example.com")
        with self.assertRaises(Exception):
            ShortURL.objects.create(short_key="abc", url="http://example.com")

    def test_duplicate_url(self):
        ShortURL.objects.create(short_key="abc", url="http://example.com")
        with self.assertRaises(Exception):
            ShortURL.objects.create(short_key="def", url="http://example.com")

    def test_str(self):
        obj = ShortURL.objects.create(short_key="abc", url="http://example.com")
        self.assertEqual(str(obj), "abc")
