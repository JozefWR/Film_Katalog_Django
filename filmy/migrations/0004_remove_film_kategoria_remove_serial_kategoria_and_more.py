# Generated by Django 5.0.4 on 2024-04-17 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmy', '0003_remove_serial_rezyser_ocenaserial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='kategoria',
        ),
        migrations.RemoveField(
            model_name='serial',
            name='kategoria',
        ),
        migrations.AddField(
            model_name='film',
            name='kategorie',
            field=models.ManyToManyField(related_name='filmy', to='filmy.kategoria'),
        ),
        migrations.AddField(
            model_name='serial',
            name='kategorie',
            field=models.ManyToManyField(related_name='seriale', to='filmy.kategoria'),
        ),
    ]