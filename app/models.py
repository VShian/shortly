import random

from django.conf import settings
from django.db import models


class ShortURL(models.Model):
    short_key = models.CharField(max_length=100, primary_key=True)
    url = models.URLField(max_length=2048, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.short_key

    @staticmethod
    def generate_short_key(length=settings.SHORT_KEY_LENGTH, failed_attempts=0):
        if failed_attempts > settings.MAX_SHORT_KEY_ATTEMPTS:
            return ShortURL.generate_short_key(
                length=settings.SHORT_KEY_LENGTH * 2,
                failed_attempts=failed_attempts + 1,
            )

        chars = "abcdefghijklmnpqrstuvwxyz123456789"
        key = "".join(random.choices(chars, k=length))

        if ShortURL.objects.filter(short_key=key).exists():
            return ShortURL.generate_short_key(failed_attempts=failed_attempts + 1)

        return key
