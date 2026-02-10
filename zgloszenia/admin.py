from django.contrib import admin
from .models import Zgloszenie 

@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'priorytet', 'status', 'data_utworzenia')
    list_filter = ('status', 'kategoria', 'priorytet')
    search_fields = ('tytul', 'opis')
