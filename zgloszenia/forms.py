from django import forms
from .models import Komentarz, Zgloszenie, Sprzet

class ZgloszenieForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ['tytul', 'urzadzenie', 'opis', 'priorytet']

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if user:
                self.fields['urzadzenie'].queryset = Sprzet.objects.filter(wlasciciel=user)

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
        
        widgets = {
            'tresc': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }