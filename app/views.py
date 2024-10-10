from django.urls import reverse
from rest_framework import mixins, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortURL
from .serializers import URLSerializer


class ShortURLViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = ShortURL.objects.all()
    serializer_class = URLSerializer


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"
    authentication_classes = []

    def get(self, request):
        return Response()

    def post(self, request):
        short_key = ShortURL.generate_short_key()
        url = request.POST.get("url")

        try:
            obj, _ = ShortURL.objects.get_or_create(
                url=url, defaults={"short_key": short_key}
            )
            reverse_url = reverse("redirect-url", kwargs={"short_key": obj.short_key})
            absolute_url = request.build_absolute_uri(reverse_url)
            return Response({"short_url": absolute_url, "url": obj.url})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
