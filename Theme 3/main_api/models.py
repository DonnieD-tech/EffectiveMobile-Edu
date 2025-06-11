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