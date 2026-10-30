from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MuseumViewSet

router = DefaultRouter()
router.register(r'museums', MuseumViewSet)

urlpatterns = [
    path('', include(router.urls)),
]