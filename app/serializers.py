from rest_framework import serializers

from .models import ShortURL


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = [
            "short_key",
            "url",
        ]
        read_only_fields = ["short_key"]

    def create(self, validated_data):
        short_key = ShortURL.generate_short_key()
        return ShortURL.objects.create(short_key=short_key, **validated_data)
