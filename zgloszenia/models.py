from django.db import models
from django.contrib.auth.models import User

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

    autor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tytul} - ({self.status})"
    
    class Meta:
        verbose_name = 'Zgłoszenie'
        verbose_name_plural = 'Zgłoszenia'