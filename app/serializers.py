from rest_framework import serializers

from .models import ShortURL
from .utils import generate_short_key
from .utils import get_short_url as get_short_url_util


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = [
            "short_url",
            "short_key",
            "url",
        ]
        read_only_fields = [
            "short_url",
            "short_key",
        ]

    def get_short_url(self, obj):
        return get_short_url_util(obj, self.context["request"])

    def create(self, validated_data):
        short_key = generate_short_key()
        return ShortURL.objects.create(short_key=short_key, **validated_data)
