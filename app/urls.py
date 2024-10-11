from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import HomeView, RedirectView, ShortURLViewSet

router = DefaultRouter()
router.register(r"short-url", ShortURLViewSet, basename="short-url")

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    re_path(r"^api/", include(router.urls)),
    path("r/<str:short_key>/", RedirectView.as_view(), name="redirect-url"),
]
