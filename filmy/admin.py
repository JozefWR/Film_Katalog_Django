from django.contrib import admin
from .models import Kategoria, Film, Ocena, Serial, OcenaSerial

@admin.register(Kategoria)
class KategoriaAdmin(admin.ModelAdmin):
    list_display = ['nazwa']

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['tytul', 'rezyser', 'rok_wydania', 'display_kategorie']
    list_filter = [('kategorie', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['tytul', 'rezyser']

    def display_kategorie(self, obj):
        return ", ".join([k.nazwa for k in obj.kategorie.all()])
    display_kategorie.short_description = 'Kategorie'

@admin.register(Ocena)
class OcenaAdmin(admin.ModelAdmin):
    list_display = ['film', 'uzytkownik', 'ocena']
    list_filter = ['film', 'uzytkownik']


@admin.register(OcenaSerial)
class OcenaSerialAdmin(admin.ModelAdmin):
    list_display = ['serial', 'uzytkownik', 'ocena']
    list_filter = ['serial', 'uzytkownik']

@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ['tytul', 'poczatek_emisji', 'koniec_emisji', 'emisja_trwa', 'display_kategorie']
    list_filter = [('kategorie', admin.RelatedOnlyFieldListFilter)]
    search_fields = ['tytul']

    def display_kategorie(self, obj):
        return ", ".join([k.nazwa for k in obj.kategorie.all()])
    display_kategorie.short_description = 'Kategorie'

    def emisja_trwa(self, obj):
        return obj.koniec_emisji is None
    emisja_trwa.boolean = True
    emisja_trwa.short_description = 'Emisja trwa?'
