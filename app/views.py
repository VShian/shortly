from django.shortcuts import render
from rest_framework import mixins, viewsets

from .models import ShortURL
from .serializers import URLSerializer


class ShortURLViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = ShortURL.objects.all()
    serializer_class = URLSerializer
