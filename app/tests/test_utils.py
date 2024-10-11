from unittest.mock import Mock, patch

from django.conf import settings
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from app.utils import generate_short_key, get_short_url


@override_settings(ALLOWED_HOSTS=["example.com", "sub.example.com"])
class GetShortURLTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.mock_obj = Mock()
        self.mock_obj.short_key = "abc123"

    def test_get_short_url_http(self):
        request = self.factory.get("/test/", HTTP_HOST="example.com")
        url = get_short_url(self.mock_obj, request)
        expected_url = "http://example.com" + reverse("redirect-url", args=["abc123"])
        self.assertEqual(url, expected_url)

    def test_get_short_url_https(self):
        request = self.factory.get("/test/", HTTP_HOST="example.com", secure=True)
        url = get_short_url(self.mock_obj, request)
        expected_url = "https://example.com" + reverse("redirect-url", args=["abc123"])
        self.assertEqual(url, expected_url)

    def test_get_short_url_with_subdomain(self):
        request = self.factory.get("/test/", HTTP_HOST="sub.example.com")
        url = get_short_url(self.mock_obj, request)
        expected_url = "http://sub.example.com" + reverse(
            "redirect-url", args=["abc123"]
        )
        self.assertEqual(url, expected_url)

    @patch("app.utils.reverse")
    def test_get_short_url_reverse_call(self, mock_reverse):
        mock_reverse.return_value = "/r/abc123"
        request = self.factory.get("/test/", HTTP_HOST="example.com")
        url = get_short_url(self.mock_obj, request)
        mock_reverse.assert_called_once_with("redirect-url", args=["abc123"])
        self.assertEqual(mock_reverse.call_count, 1)
        self.assertEqual(url, "http://example.com/r/abc123")


class GenerateShortKeyTestCase(TestCase):
    @patch("app.utils.ShortURL.objects.filter")
    def test_generate_short_key_length(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        key = generate_short_key()
        self.assertEqual(len(key), settings.SHORT_KEY_LENGTH)

    @patch("app.utils.ShortURL.objects.filter")
    def test_generate_short_key_unique(self, mock_filter):
        mock_filter.return_value.exists.side_effect = [True, False]
        key = generate_short_key()
        self.assertEqual(mock_filter.call_count, 2)

    @patch("app.utils.ShortURL.objects.filter")
    @override_settings(MAX_SHORT_KEY_ATTEMPTS=3, SHORT_KEY_LENGTH=5)
    def test_generate_short_key_max_attempts(self, mock_filter):
        mock_filter.return_value.exists.side_effect = [True, True, True, False]
        key = generate_short_key(length=5)
        self.assertEqual(mock_filter.call_count, 4)
        self.assertEqual(len(key), 10)

    @patch("app.utils.ShortURL.objects.filter")
    def test_generate_short_key_custom_length(self, mock_filter):
        mock_filter.return_value.exists.return_value = False
        key = generate_short_key(length=10)
        self.assertEqual(len(key), 10)
