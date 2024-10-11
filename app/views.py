from rest_framework import mixins, status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortURL
from .serializers import URLSerializer
from .utils import generate_short_key, get_short_url


class ShortURLViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ShortURL.objects.all()
    serializer_class = URLSerializer

    def list(self, request, *args, **kwargs):
        url = request.query_params.get("url")

        if not url:
            return Response(
                {"detail": "URL query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if ShortURL.objects.filter(url=url).exists():
            obj = ShortURL.objects.get(url=url)
            serializer = self.serializer_class(obj, context={"request": request})
            return Response(serializer.data)

        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        url = request.data.get("url")
        if ShortURL.objects.filter(url=url).exists():
            obj = ShortURL.objects.get(url=url)
            serializer = self.serializer_class(obj, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)


class RedirectView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    authentication_classes = []
    template_name = "redirect.html"

    def get(self, request, short_key):
        try:
            obj = ShortURL.objects.get(short_key=short_key)
            return Response({"url": obj.url})
        except ShortURL.DoesNotExist:
            return Response({}, template_name="404.html")


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"
    authentication_classes = []

    def get(self, request):
        return Response()

    def post(self, request):
        short_key = generate_short_key()
        url = request.POST.get("url")

        obj, _ = ShortURL.objects.get_or_create(
            url=url, defaults={"short_key": short_key}
        )

        return Response({"short_url": get_short_url(obj, self.request), "url": obj.url})
