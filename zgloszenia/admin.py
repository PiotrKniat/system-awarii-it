from django.contrib import admin
from .models import Zgloszenie, Sprzet, Komentarz

@admin.register(Sprzet)
class SprzetAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'numer_seryjny', 'wlasciciel')
    search_fields = ('nazwa', 'numer_seryjny')
    list_filter = ('wlasciciel',)

@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'urzadzenie', 'priorytet', 'status', 'data_utworzenia')
    list_filter = ('status', 'kategoria', 'priorytet')
    search_fields = ('tytul', 'opis')

@admin.register(Komentarz)
class KomentarzAdmin(admin.ModelAdmin):
    list_display = ('autor', 'zgloszenie', 'data_dodania')
    list_filter = ('data_dodania', 'autor')