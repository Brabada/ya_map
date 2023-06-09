# Generated by Django 4.2.2 on 2023-06-18 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['order'], 'verbose_name': 'изображение', 'verbose_name_plural': 'изображения'},
        ),
        migrations.AddField(
            model_name='image',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
