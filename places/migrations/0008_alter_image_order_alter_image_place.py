# Generated by Django 4.2.2 on 2023-09-10 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_alter_image_image_alter_place_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='order',
            field=models.PositiveIntegerField(blank=True, db_index=True, default=0, null=True, verbose_name='Порядок'),
        ),
        migrations.AlterField(
            model_name='image',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='places.place', verbose_name='Фотографии места'),
        ),
    ]
