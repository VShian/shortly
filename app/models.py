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
