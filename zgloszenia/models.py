from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Sprzet(models.Model):
    nazwa = models.CharField(max_length=100)
    numer_seryjny = models.CharField(max_length=50, unique=True)
    wlasciciel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='zasoby')

    def __str__(self):
        return f"{self.nazwa} ({self.numer_seryjny})"

class Zgloszenie(models.Model):

    KATEGORIE = [
        ('sprzet', 'Sprzęt'),
        ('oprogramowanie', 'Oprogramowanie'),
        ('net', 'Internet'),
    ]

    PRIORYTETY = [
        ('niski', 'Niski'),
        ('wysoki', 'Wysoki'),
    ]

    STATUSY = [
        ('nowe', 'Nowe'),
        ('w_trakcie', 'W trakcie'),
        ('zamkniete', 'Zamknięte'),
    ]

    tytul = models.CharField(max_length=200, verbose_name='Tytuł awarii')
    opis = models.TextField(verbose_name='Opis awarii')
    kategoria = models.CharField(max_length=20, choices=KATEGORIE, default='sprzet')
    priorytet = models.CharField(max_length=20, choices=PRIORYTETY, default='niski')
    status = models.CharField(max_length=20, choices=STATUSY, default='nowe')
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_rozwiazania = models.DateTimeField(null=True, blank=True, verbose_name='Data rozwiązania')
    sla_deadline = models.DateTimeField(null=True, blank=True, verbose_name='Termin SLA')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='przydzielone_zgloszenia', verbose_name='Przydzielono do')
    urzadzenie = models.ForeignKey(Sprzet, on_delete=models.SET_NULL, null=True, blank=True)
    def save(self, *args, **kwargs):
        """Oblicza termin SLA przy tworzeniu zgłoszenia"""
        if not self.pk:  # Tylko przy tworzeniu nowego zgłoszenia
            self.calculate_sla_deadline()
        
        # Jeśli status zmienia się na zamknięte, zapisz czas rozwiązania
        if self.status == 'zamkniete' and not self.data_rozwiazania:
            self.data_rozwiazania = timezone.now()
        
        super().save(*args, **kwargs)
    
    def calculate_sla_deadline(self):
        """Oblicza termin SLA na podstawie priorytetu"""
        if self.priorytet == 'wysoki':
            hours = 2
        elif self.priorytet == 'niski':
            hours = 8
        else:
            hours = 8
        
        self.sla_deadline = timezone.now() + timedelta(hours=hours)
    
    def get_sla_status(self):
        """Zwraca status SLA: 'on_track', 'at_risk', 'breached'"""
        if not self.sla_deadline:
            return 'on_track'
        
        if self.status == 'zamkniete':
            if self.data_rozwiazania and self.data_rozwiazania <= self.sla_deadline:
                return 'met'
            else:
                return 'breached'
        else:
            time_remaining = self.sla_deadline - timezone.now()
            if time_remaining.total_seconds() < 0:
                return 'breached'
            elif time_remaining.total_seconds() < 3600:
                return 'at_risk'
            else:
                return 'on_track'
    
    def get_sla_status_display(self):
        """Zwraca czytelny opis statusu SLA"""
        status_map = {
            'on_track': 'W trakcie ✓',
            'at_risk': 'Zagrożenie ⚠',
            'breached': 'Przekroczone ✗',
            'met': 'Spełnione ✓'
        }
        return status_map.get(self.get_sla_status(), 'Nieznany')
    
    def get_time_remaining(self):
        """Zwraca pozostały czas do terminu SLA"""
        if not self.sla_deadline:
            return 'Brak SLA'
        
        remaining = self.sla_deadline - timezone.now()
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m"

    screenshot = models.ImageField(upload_to='screenshoty/', null=True, blank=True)

class Komentarz(models.Model):
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE, related_name='komentarze')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentarz od {self.autor.username} do {self.zgloszenie.tytul}"
    
    class Meta:
        verbose_name = 'Komentarz'
        verbose_name_plural = 'Komentarze'