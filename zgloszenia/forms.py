from django import forms
from .models import Zgloszenie

class ZgloszenieForm(forms.ModelForm):
    class Meta:
        model = Zgloszenie
        
        fields = ['tytul', 'opis', 'kategoria', 'priorytet']
        
        widgets = {
            'tytul': forms.TextInput(attrs={'class': 'form-control'}),
            'opis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'kategoria': forms.Select(attrs={'class': 'form-select'}),
            'priorytet': forms.Select(attrs={'class': 'form-select'}),
        }