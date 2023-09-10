from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    description_short = models.TextField(
        'Краткое описание',
        blank=True,
    )
    description_long = HTMLField(
        'Полное описание',
        blank=True,
    )
    longitude = models.DecimalField(
        'Долгота',
        decimal_places=7,
        max_digits=10,
    )
    latitude = models.DecimalField(
        'Широта',
        decimal_places=7,
        max_digits=10,
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'
        unique_together = ['longitude', 'latitude']

    def __str__(self):
        return f'{self.id}. {self.title}'


class Image(models.Model):
    image = models.ImageField(
        'Изображение',
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Фотографии места',
    )
    order = models.PositiveIntegerField(
        'Порядок',
        db_index=True,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return f'{self.id} {self.place.title}'
