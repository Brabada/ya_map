from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class Place(models.Model):
    title = models.CharField('Название',
                             max_length=200,
                             blank=False)
    description_short = models.TextField(
        'Краткое описание',
        blank=True)
    description_long = HTMLField(
        'Полное описание',
        blank=True)
    longitude = models.DecimalField(
        'Долгота',
        decimal_places=14,
        max_digits=17,
        null=True)
    latitude = models.DecimalField(
        'Широта',
        decimal_places=14,
        max_digits=17,
        null=True)

    def __str__(self):
        return f'{self.id}. {self.title}'

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'


class Image(models.Model):
    image = models.ImageField(
        'Изображение',
        null=True,
    )
    place = models.ForeignKey(
        Place,
        null=True,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Фотографии места',
    )
    order = models.PositiveIntegerField(
        'Порядок',
        default=0,
        db_index=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.place.title

    class Meta:
        ordering = ['order']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
