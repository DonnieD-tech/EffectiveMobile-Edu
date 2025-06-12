from rest_framework import serializers

from .models import Breed, Dog


class BreedSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Breed."""

    dog_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = "__all__"


class DogSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Dog."""

    breed_name = serializers.CharField(source="breed.name", read_only=True)
    same_breed_count = serializers.IntegerField(read_only=True)
    avg_age_by_breed = serializers.FloatField(read_only=True)

    class Meta:
        model = Dog
        fields = [
            "id",
            "name",
            "age",
            "breed",
            "gender",
            "color",
            "favorite_food",
            "favorite_toy",
            "breed_name",
            "same_breed_count",
            "avg_age_by_breed"
        ]
