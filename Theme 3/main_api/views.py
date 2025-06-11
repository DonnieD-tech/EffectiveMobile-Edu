from django.db.models import Count, OuterRef, Subquery
from rest_framework import viewsets

from .models import Breed, Dog
from .serializers import BreedSerializer, DogSerializer


class BreedViewSet(viewsets.ModelViewSet):
    """ViewSet для управления объектами модели Breed.

    Позволяет выполнять операции:
    - Получение списка пород
    - Создание новой породы
    - Получение, обновление и удаление конкретной породы
    """

    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    def get_queryset(self):
        """Возвращает queryset с аннотацией dog_count — количество собак данной породы."""

        return Breed.objects.annotate(dog_count=Count("dogs"))
