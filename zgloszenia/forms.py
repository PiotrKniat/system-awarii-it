from django import forms
from .models import Komentarz, Zgloszenie, Sprzet

class ZgloszenieForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        fields = ['tytul', 'urzadzenie', 'kategoria', 'opis', 'priorytet']

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if user:
                self.fields['urzadzenie'].queryset = Sprzet.objects.filter(wlasciciel=user)
                self.fields['urzadzenie'].empty_label = "--- Wybierz sprzęt (opcjonalnie) ---"

            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'})

class KomentarzForm(forms.ModelForm):
    class Meta:
        model = Komentarz
        fields = ['tresc']
        widgets = {
            'tresc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dodaj odpowiedź...'})
        }

class SprzetForm(forms.ModelForm):
    class Meta:
        model = Sprzet
        fields = ['nazwa', 'numer_seryjny', 'wlasciciel']
        widgets = {
            'nazwa': forms.TextInput(attrs={'class': 'form-control'}),
            'numer_seryjny': forms.TextInput(attrs={'class': 'form-control'}),
            'wlasciciel': forms.Select(attrs={'class': 'form-select'}),
        }