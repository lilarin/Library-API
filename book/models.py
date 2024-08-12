from django.db import models
from django.core.validators import MinValueValidator


class Book(models.Model):
    class CoverType(models.TextChoices):
        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=CoverType.choices,
    )
    inventory = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    daily_fee = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(0.09)]
    )  # MinValueValidator = 0.09 because 0.1 does not allow to set as 0.1

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f'"{self.title}" by {self.author}'
