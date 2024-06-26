# Generated by Django 5.0.4 on 2024-04-24 12:50

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmy', '0005_alter_film_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='ocena',
            name='ocena',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='ocenaserial',
            name='ocena',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterUniqueTogether(
            name='ocena',
            unique_together={('film', 'uzytkownik')},
        ),
        migrations.AlterUniqueTogether(
            name='ocenaserial',
            unique_together={('serial', 'uzytkownik')},
        ),
    ]
