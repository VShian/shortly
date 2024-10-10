from rest_framework.routers import DefaultRouter

from .views import ShortURLViewSet

router = DefaultRouter()
router.register(r"api/short-url", ShortURLViewSet)

urlpatterns = router.urls
