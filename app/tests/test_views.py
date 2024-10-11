from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from app.models import ShortURL


class ShortURLViewSetTestCase(APITestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.obj = ShortURL.objects.create(url=self.url, short_key="abc123")

    def test_create_new_short_url(self):
        data = {"url": "https://new-example.com"}
        response = self.client.post(reverse("short-url-list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ShortURL.objects.filter(url=data["url"]).exists())

    def test_create_existing_short_url(self):
        data = {"url": self.url}
        response = self.client.post(reverse("short-url-list"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["url"], self.url)

    def test_retrieve_short_url(self):
        response = self.client.get(
            reverse("short-url-detail", kwargs={"pk": self.obj.short_key})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["url"], self.url)


class RedirectViewTestCase(TestCase):
    def setUp(self):
        self.url = "https://example.com"
        self.obj = ShortURL.objects.create(url=self.url, short_key="abc123")

    def test_redirect_valid_short_key(self):
        response = self.client.get(
            reverse("redirect-url", kwargs={"short_key": "abc123"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "redirect.html")
        self.assertEqual(response.context["url"], self.url)

    def test_redirect_invalid_short_key(self):
        response = self.client.get(
            reverse("redirect-url", kwargs={"short_key": "invalid"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "404.html")


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.url = "https://example.com"

    def test_get_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    @patch("app.views.generate_short_key", return_value="abc123")
    def test_create_short_url(self, mock_generate_short_key):
        data = {"url": self.url}
        response = self.client.post(reverse("home"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_url", response.context)
        self.assertIn("url", response.context)
        self.assertEqual(response.context["url"], self.url)
        self.assertEqual(response.context["short_url"], f"http://testserver/r/abc123/")
        self.assertTrue(ShortURL.objects.filter(url=self.url).exists())

    def test_get_existing_short_url(self):
        ShortURL.objects.create(url=self.url, short_key="abc123")
        data = {"url": self.url}
        response = self.client.post(reverse("home"), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("short_url", response.context)
        self.assertIn("url", response.context)
        self.assertEqual(response.context["url"], self.url)
        self.assertEqual(response.context["short_url"], f"http://testserver/r/abc123/")
        self.assertEqual(ShortURL.objects.filter(url=self.url).count(), 1)
        self.assertEqual(ShortURL.objects.count(), 1)
