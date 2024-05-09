from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

class Kategoria(models.Model):
    nazwa = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nazwa

class Film(models.Model):
    tytul = models.CharField(max_length=255)
    rezyser = models.CharField(max_length=100)
    rok_wydania = models.IntegerField()
    opis = models.TextField()
    kategorie = models.ManyToManyField(Kategoria, related_name='filmy')

    class Meta:
        unique_together = ('tytul', 'rezyser', 'rok_wydania')

    def __str__(self):
        return self.tytul

class Serial(models.Model):
    tytul = models.CharField(max_length=255)
    opis = models.TextField()
    poczatek_emisji = models.IntegerField()
    koniec_emisji = models.IntegerField(blank=True, null=True)
    kategorie = models.ManyToManyField(Kategoria, related_name='seriale')

    class Meta:
        unique_together = ('tytul', 'poczatek_emisji')

    def __str__(self):
        return f"{self.tytul} (od {self.poczatek_emisji})"

class Ocena(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='oceny')
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ['film', 'uzytkownik']

    def __str__(self):
        return f"{self.ocena} / 5 - {self.film.tytul}"

class OcenaSerial(models.Model):
    serial = models.ForeignKey(Serial, on_delete=models.CASCADE, related_name='oceny')
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ['serial', 'uzytkownik']

    def __str__(self):
        return f"{self.ocena} / 5 - {self.serial.tytul}"
    
    