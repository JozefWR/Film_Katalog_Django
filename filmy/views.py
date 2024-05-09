from django.shortcuts import render
from django.db.models import Q
from django.db.models import Avg
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Kategoria, Film, Serial
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login
from .models import Ocena, Film, Serial, OcenaSerial
from .forms import OcenaFilmuForm, OcenaSerialuForm
from django.db.models import Exists, OuterRef, Subquery


def strona_glowna(request):
    najlepsze_filmy = Film.objects.annotate(
        srednia_ocena=Avg('oceny__ocena')
    ).order_by('-srednia_ocena')[:5]

    najlepsze_seriale = Serial.objects.annotate(
        srednia_ocena=Avg('oceny__ocena')
    ).order_by('-srednia_ocena')[:5]

    if request.user.is_authenticated:
        oceny_filmy = Ocena.objects.filter(uzytkownik=request.user, film=OuterRef('pk'))
        oceny_seriale = OcenaSerial.objects.filter(uzytkownik=request.user, serial=OuterRef('pk'))
        najlepsze_filmy = najlepsze_filmy.annotate(
            ocena_istnieje=Exists(oceny_filmy),
            ocena_uzytkownika=Subquery(oceny_filmy.values('ocena')[:1])
        )
        najlepsze_seriale = najlepsze_seriale.annotate(
            ocena_istnieje=Exists(oceny_seriale),
            ocena_uzytkownika=Subquery(oceny_seriale.values('ocena')[:1])
        )

    return render(request, 'filmy/strona_glowna.html', {
        'najlepsze_filmy': najlepsze_filmy,
        'najlepsze_seriale': najlepsze_seriale
    })


def lista_filmow(request):
    sort_by = request.GET.get('sort', 'tytul')
    if sort_by not in ['tytul', 'rok_wydania', 'kategorie__nazwa']:
        sort_by = 'tytul'

    filmy = Film.objects.all().order_by(sort_by)
    filmy_oceny = []

    for film in filmy:
        if request.user.is_authenticated:
            ocena_istnieje = film.oceny.filter(uzytkownik=request.user).exists()
            ocena = film.oceny.get(uzytkownik=request.user).ocena if ocena_istnieje else None
        else:
            ocena_istnieje = False
            ocena = None

        filmy_oceny.append({
            'film': film,
            'ocena_istnieje': ocena_istnieje,
            'ocena': ocena
        })
    return render(request, 'filmy/lista_filmow.html', {'filmy_oceny': filmy_oceny})


def lista_seriali(request):
    sort_by = request.GET.get('sort', 'tytul')  
    if sort_by not in ['tytul', 'poczatek_emisji', 'kategorie__nazwa']:
        sort_by = 'tytul'  
    
    seriale = Serial.objects.all().order_by(sort_by)
    seriale_oceny = []

    for serial in seriale:
        if request.user.is_authenticated:
            ocena_istnieje = OcenaSerial.objects.filter(uzytkownik=request.user, serial=serial).exists()
            ocena = OcenaSerial.objects.filter(uzytkownik=request.user, serial=serial).first().ocena if ocena_istnieje else None
        else:
            ocena_istnieje = False
            ocena = None

        seriale_oceny.append({
            'serial': serial,
            'ocena_istnieje': ocena_istnieje,
            'ocena': ocena
        })
    return render(request, 'filmy/lista_seriali.html', {'seriale_oceny': seriale_oceny})

def najlepsze_filmy(request):
    kategorie = Kategoria.objects.all()
    najlepsze_filmy_w_kategorii = {}

    for kategoria in kategorie:
        filmy_w_kategorii = Film.objects.filter(
            kategorie=kategoria
        ).annotate(
            srednia_ocena=Avg('oceny__ocena'),
            liczba_ocen=Count('oceny')
        ).filter(
            liczba_ocen__gt=0
        ).order_by('-srednia_ocena')[:5]

        if request.user.is_authenticated:
            oceny_filmy = Ocena.objects.filter(
                uzytkownik=request.user,
                film=OuterRef('pk')
            )
            filmy_w_kategorii = filmy_w_kategorii.annotate(
                ocena_istnieje=Exists(oceny_filmy),
                ocena_uzytkownika=Subquery(oceny_filmy.values('ocena')[:1])
            )

        if filmy_w_kategorii.exists():
            najlepsze_filmy_w_kategorii[kategoria.nazwa] = filmy_w_kategorii
    return render(request, 'filmy/najlepsze_filmy.html', {
        'najlepsze_w_kategorii': najlepsze_filmy_w_kategorii
    })

def najlepsze_seriale(request):
    kategorie = Kategoria.objects.all()
    najlepsze_seriale_w_kategorii = {}

    for kategoria in kategorie:
        seriale_w_kategorii = Serial.objects.filter(
            kategorie=kategoria
        ).annotate(
            srednia_ocena=Avg('oceny__ocena'),
            liczba_ocen=Count('oceny')
        ).filter(
            liczba_ocen__gt=0
        ).order_by('-srednia_ocena')[:5]

        if request.user.is_authenticated:
            oceny_seriale = OcenaSerial.objects.filter(
                uzytkownik=request.user,
                serial=OuterRef('pk')
            )
            seriale_w_kategorii = seriale_w_kategorii.annotate(
                ocena_istnieje=Exists(oceny_seriale),
                ocena_uzytkownika=Subquery(oceny_seriale.values('ocena')[:1])
            )

        if seriale_w_kategorii.exists():
            najlepsze_seriale_w_kategorii[kategoria.nazwa] = seriale_w_kategorii

    return render(request, 'filmy/najlepsze_seriale.html', {
        'najlepsze_w_kategorii': najlepsze_seriale_w_kategorii
    })

def wyszukaj(request):
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'tytul')
    
    if query:
        filmy = Film.objects.filter(
            Q(tytul__icontains=query) | 
            Q(rezyser__icontains=query)
        )
        seriale = Serial.objects.filter(
            Q(tytul__icontains=query) 
        )

        if sort_by == 'rok_wydania':
            filmy = filmy.order_by('rok_wydania')
            seriale = seriale.order_by('poczatek_emisji')
        elif sort_by == 'kategorie__nazwa':
            filmy = filmy.order_by('kategorie__nazwa')
            seriale = seriale.order_by('kategorie__nazwa')
        else:
            filmy = filmy.order_by('tytul')
            seriale = seriale.order_by('tytul')
        
        if request.user.is_authenticated:
            oceny_filmy = Ocena.objects.filter(uzytkownik=request.user, film=OuterRef('pk'))
            filmy = filmy.annotate(
                ocena_istnieje=Exists(oceny_filmy),
                ocena_uzytkownika=Subquery(oceny_filmy.values('ocena')[:1])
            )
            
            oceny_seriale = OcenaSerial.objects.filter(uzytkownik=request.user, serial=OuterRef('pk'))
            seriale = seriale.annotate(
                ocena_istnieje=Exists(oceny_seriale),
                ocena_uzytkownika=Subquery(oceny_seriale.values('ocena')[:1])
            )

        filmy = filmy.distinct()
        seriale = seriale.distinct()
    else:
        filmy = Film.objects.none()
        seriale = Serial.objects.none()

    return render(request, 'filmy/wyniki_wyszukiwania.html', {
        'filmy': filmy, 'seriale': seriale, 'query': query, 'sort_by': sort_by
    })

def szczegoly_ajax(request, id):
    film = get_object_or_404(Film, id=id)
    film_srednia_ocena = film.oceny.aggregate(Avg('ocena'))['ocena__avg']
    context = {
        'film': film,
        'srednia_ocena': film_srednia_ocena,
    }
    html = render_to_string('filmy/fragment_szczegolow_filmu.html', context)
    return HttpResponse(html)

def szczegoly_serial_ajax(request, id):
    serial = get_object_or_404(Serial, id=id)
    serial_srednia_ocena = serial.oceny.aggregate(Avg('ocena'))['ocena__avg']
    context = {
        'serial': serial,
        'srednia_ocena': serial_srednia_ocena,
    }
    html = render_to_string('filmy/fragment_szczegoly_serial.html', context)
    return HttpResponse(html)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('strona_glowna')
    else:
        form = UserCreationForm()
    return render(request, 'filmy/register.html', {'form': form})

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('strona_glowna')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

def dodaj_ocene_filmu(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    ocena_istniejaca = film.oceny.filter(uzytkownik=request.user).first()
    if ocena_istniejaca:
        
        return redirect('zmien_ocene_filmu', film_id=film_id)
    
    if request.method == 'POST':
        form = OcenaFilmuForm(request.POST)
        if form.is_valid():
            ocena = form.save(commit=False)
            ocena.film = film
            ocena.uzytkownik = request.user
            ocena.save()
            return redirect('strona_glowna')
    else:
        form = OcenaFilmuForm()

    return render(request, 'filmy/formularz_oceny.html', {'form': form, 'film': film})

def zmien_ocene_filmu(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    ocena = film.oceny.get(uzytkownik=request.user)
    if request.method == 'POST':
        form = OcenaFilmuForm(request.POST, instance=ocena)
        if form.is_valid():
            form.save()
            return redirect('strona_glowna')
    else:
        form = OcenaFilmuForm(instance=ocena)
    return render(request, 'filmy/formularz_oceny.html', {'form': form, 'film': film})

def dodaj_ocene_serialu(request, serial_id):
    serial = get_object_or_404(Serial, pk=serial_id)
    if request.method == 'POST':
        form = OcenaSerialuForm(request.POST)
        if form.is_valid():
            ocena = form.save(commit=False)
            ocena.serial = serial
            ocena.uzytkownik = request.user
            ocena.save()
            return redirect('strona_glowna')
    else:
        form = OcenaSerialuForm()
    return render(request, 'filmy/formularz_oceny_serialu.html', {'form': form, 'serial': serial})

def zmien_ocene_serialu(request, serial_id):
    serial = get_object_or_404(Serial, pk=serial_id)
    ocena = serial.oceny.get(uzytkownik=request.user)
    if request.method == 'POST':
        form = OcenaSerialuForm(request.POST, instance=ocena)
        if form.is_valid():
            form.save()
            return redirect('strona_glowna')
    else:
        form = OcenaSerialuForm(instance=ocena)
    return render(request, 'filmy/formularz_oceny_serialu.html', {'form': form, 'serial': serial})