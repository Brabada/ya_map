from django.db import models

# Create your models here.


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField(
        'Краткое описание',
        blank=True)
    description_long = models.TextField(
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
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'место'
        verbose_name_plural = 'места'
