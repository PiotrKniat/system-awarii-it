from django import forms
from .models import Komentarz, Zgloszenie, Sprzet
from django.contrib.auth.models import User

class ZgloszenieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['urzadzenie'].queryset = Sprzet.objects.filter(wlasciciel=user)
            self.fields['urzadzenie'].empty_label = "--- Wybierz sprzęt (opcjonalnie) ---"
        
        self.fields['screenshot'].widget.attrs.update({'class': 'form-control'})
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Zgloszenie
        fields = ['tytul', 'urzadzenie', 'kategoria', 'opis', 'priorytet', 'screenshot']


class ZgloszenieAssignmentForm(forms.ModelForm):
    """Form dla adminów do przydzielania zgłoszeń"""
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=False,
        empty_label="--- Bez przydzielenia ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Zgloszenie
        fields = ['assigned_to', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

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