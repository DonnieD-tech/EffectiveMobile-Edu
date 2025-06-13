from django.db.models import Avg, Count, OuterRef, Subquery
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


class DogViewSet(viewsets.ModelViewSet):
    """ViewSet для управления объектами модели Dog.

    Позволяет выполнять операции:
    - Получение списка собак
    - Создание новой собаки
    - Получение, обновление и удаление конкретной собаки
    """

    queryset = Dog.objects.all()
    serializer_class = DogSerializer

    def get_queryset(self):
        """Возвращает queryset с аннотациями:
        - breed_name: имя породы
        - same_breed_count: количество собак той же породы
        """

        same_breed_count = (
            Dog.objects.filter(breed=OuterRef("breed"))
            .values("breed")
            .annotate(count=Count("id")).values("count")
        )

        avg_age_by_breed = (
            Dog.objects.filter(breed=OuterRef("breed"))
            .values("breed")
            .annotate(avg_age=Avg("age"))
            .values("avg_age")
        )

        return Dog.objects.annotate(
            same_breed_count=Subquery(same_breed_count[:1]),
            breed_name=Subquery(Breed.objects.filter(id=OuterRef("breed_id")).values("name")[:1]),
            avg_age_by_breed=Subquery(avg_age_by_breed[:1]),
        )
