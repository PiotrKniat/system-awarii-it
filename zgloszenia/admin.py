from django.contrib import admin
from .models import Zgloszenie, Sprzet, Komentarz

@admin.register(Sprzet)
class SprzetAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'numer_seryjny', 'wlasciciel')
    search_fields = ('nazwa', 'numer_seryjny')
    list_filter = ('wlasciciel',)

@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'autor', 'assigned_to', 'priorytet', 'status', 'sla_status_colored', 'time_to_sla', 'data_utworzenia')
    list_filter = ('status', 'kategoria', 'priorytet', 'assigned_to')
    search_fields = ('tytul', 'opis')
    readonly_fields = ('data_utworzenia', 'autor', 'sla_deadline', 'data_rozwiazania', 'sla_status_info')
    
    def sla_status_colored(self, obj):
        """Wyświetla status SLA z kolorami"""
        status = obj.get_sla_status()
        colors = {
            'on_track': '#28a745',
            'at_risk': '#ffc107',
            'breached': '#dc3545',
            'met': '#17a2b8'
        }
        color = colors.get(status, '#6c757d')
        status_display = obj.get_sla_status_display()
        return f'<span style="color: white; background-color: {color}; padding: 5px 10px; border-radius: 3px;">{status_display}</span>'
    sla_status_colored.short_description = 'Status SLA'
    sla_status_colored.allow_tags = True
    
    def time_to_sla(self, obj):
        """Wyświetla pozostały czas do terminu SLA"""
        if obj.status == 'zamkniete':
            return 'Zamknięte'
        return obj.get_time_remaining()
    time_to_sla.short_description = 'Pozostało'
    
    def sla_status_info(self, obj):
        """Wyświetla szczegółowe informacje o SLA"""
        return f"{obj.get_sla_status_display()} | Termin: {obj.sla_deadline.strftime('%Y-%m-%d %H:%M')}"
    sla_status_info.short_description = 'Informacja o SLA'
    
    fieldsets = (
        ('Podstawowe informacje', {
            'fields': ('tytul', 'opis', 'kategoria', 'autor', 'data_utworzenia')
        }),
        ('Priorytet i SLA', {
            'fields': ('priorytet', 'sla_deadline', 'sla_status_info')
        }),
        ('Przydzielenie', {
            'fields': ('assigned_to', 'urzadzenie')
        }),
        ('Status', {
            'fields': ('status', 'data_rozwiazania')
        }),
        ('Załączniki', {
            'fields': ('screenshot',)
        }),
    )

@admin.register(Komentarz)
class KomentarzAdmin(admin.ModelAdmin):
    list_display = ('autor', 'zgloszenie', 'data_dodania')
    list_filter = ('data_dodania', 'autor')