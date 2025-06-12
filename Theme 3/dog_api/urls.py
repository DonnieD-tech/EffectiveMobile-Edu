from django.urls import include, path
from rest_framework.routers import DefaultRouter

from main_api.views import BreedViewSet, DogViewSet


router = DefaultRouter()
router.register(r"dogs", DogViewSet)
router.register(r"breeds", BreedViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
