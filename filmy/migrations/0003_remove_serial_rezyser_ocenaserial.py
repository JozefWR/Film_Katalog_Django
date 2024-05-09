# Generated by Django 5.0.4 on 2024-04-17 16:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmy', '0002_serial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serial',
            name='rezyser',
        ),
        migrations.CreateModel(
            name='OcenaSerial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocena', models.PositiveSmallIntegerField()),
                ('serial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='oceny', to='filmy.serial')),
                ('uzytkownik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
