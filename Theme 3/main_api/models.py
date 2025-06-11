from django.db import models


class Breed(models.Model):
    """Модель, представляющая породу собаки.

    Атрибуты:
        name (str): Название породы.
        size (str): Размер породы (Tiny, Small, Medium, Large).
        friendliness (int): Уровень дружелюбия (от 1 до 5).
        trainability (int): Уровень обучаемости (от 1 до 5).
        shedding_amount (int): Уровень линьки (от 1 до 5).
        exercise_needs (int): Потребность в активности (от 1 до 5).
    """

    SIZE_CHOICES = [("Tiny", "Tiny"), ("Small", "Small"),
                    ("Medium", "Medium"), ("Large", "Large")]
    NUM_CHOICES = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]

    name = models.CharField(max_length=255)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    friendliness = models.PositiveSmallIntegerField(choices=NUM_CHOICES)
    trainability = models.PositiveSmallIntegerField(choices=NUM_CHOICES)
    shedding_amount = models.PositiveSmallIntegerField(choices=NUM_CHOICES)
    exercise_needs = models.PositiveSmallIntegerField(choices=NUM_CHOICES)

    def __str__(self):
        """Возвращает строковое представление породы."""

        return self.name


class Dog(models.Model):
    """Модель, представляющая собаку.

    Атрибуты:
        name (str): Имя собаки.
        age (int): Возраст собаки.
        breed (Breed): Внешний ключ на породу.
        gender (str): Пол собаки.
        color (str): Окрас собаки.
        favorite_food (str): Любимая еда собаки.
        favorite_toy (str): Любимая игрушка собаки.
    """

    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    breed = models.ForeignKey(Breed, related_name="dogs", on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    color = models.CharField(max_length=100)
    favorite_food = models.CharField(max_length=255)
    favorite_toy = models.CharField(max_length=255)

    def __str__(self):
        """Возвращает строковое представление собаки."""

        return self.name