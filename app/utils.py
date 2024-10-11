import random

from django.conf import settings
from django.urls import reverse

from app.models import ShortURL


def get_short_url(obj, request):
    reverse_url = reverse("redirect-url", args=[obj.short_key])
    return request.build_absolute_uri(reverse_url)


def generate_short_key(length=settings.SHORT_KEY_LENGTH, failed_attempts=0):
    if failed_attempts >= settings.MAX_SHORT_KEY_ATTEMPTS:
        # increase the length of the short key if max attempts exceeded
        # and retry generating the short key for the new length
        # TODO: add log here. If this happens frequently, it may indicate a problem
        # and should be investigated (we may need to increase the length of the short key)
        length = length + settings.SHORT_KEY_LENGTH
        failed_attempts = 0

    # excluded characters that can be easily confused such as letter 'o' and number '0'
    chars = "abcdefghijklmnpqrstuvwxyz123456789"
    key = "".join(random.choices(chars, k=length))

    if ShortURL.objects.filter(short_key=key).exists():
        return generate_short_key(length=length, failed_attempts=failed_attempts + 1)

    return key
