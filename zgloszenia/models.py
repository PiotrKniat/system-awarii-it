from django.db import models
from django.contrib.auth.models import User

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
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    urzadzenie = models.ForeignKey(Sprzet, on_delete=models.SET_NULL, null=True, blank=True)
    screenshot = models.ImageField(upload_to='screenshoty/', null=True, blank=True, verbose_name="Zrzut ekranu (opcjonalnie)")

class Komentarz(models.Model):
    zgloszenie = models.ForeignKey(Zgloszenie, on_delete=models.CASCADE, related_name='komentarze')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_dodania = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tytul} - ({self.status})"
    
    class Meta:
        verbose_name = 'Zgłoszenie'
        verbose_name_plural = 'Zgłoszenia'