"""
URL configuration for katalog_filmow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from filmy.views import (
    lista_filmow, lista_seriali, strona_glowna,
    najlepsze_filmy, najlepsze_seriale, wyszukaj,
    szczegoly_ajax, szczegoly_serial_ajax, register, 
    CustomLogoutView, dodaj_ocene_serialu, dodaj_ocene_filmu,
    zmien_ocene_filmu,zmien_ocene_serialu
      
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', strona_glowna, name='strona_glowna'),
    path('filmy/', lista_filmow, name='lista_filmow'),
    path('seriale/', lista_seriali, name='lista_seriali'),
    path('najlepsze-filmy/', najlepsze_filmy, name='najlepsze_filmy'),
    path('najlepsze-seriale/', najlepsze_seriale, name='najlepsze_seriale'),
    path('wyszukaj/', wyszukaj, name='wyszukaj'),
    path('ajax/szczegoly-filmu/<int:id>/', szczegoly_ajax, name='szczegoly_ajax'),
    path('ajax/szczegoly-film/<int:id>/', szczegoly_ajax, name='szczegoly_ajax_alt'),
    path('ajax/szczegoly-serial/<int:id>/', szczegoly_serial_ajax, name='szczegoly_serial_ajax'),
    path('login/', auth_views.LoginView.as_view(template_name='filmy/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('serial/<int:serial_id>/ocena/', dodaj_ocene_serialu, name='dodaj_ocene_serialu'),
    path('serial/<int:serial_id>/zmien_ocene/', zmien_ocene_serialu, name='zmien_ocene_serialu'),
    path('film/<int:film_id>/dodaj_ocene/', dodaj_ocene_filmu, name='dodaj_ocene_filmu'),
    path('film/<int:film_id>/zmien_ocene/', zmien_ocene_filmu, name='zmien_ocene_filmu'),
]


