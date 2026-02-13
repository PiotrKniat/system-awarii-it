from django.shortcuts import render, redirect, get_object_or_404
from .models import Zgloszenie
from .forms import ZgloszenieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def rejestracja(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Konto dla {username} zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def czy_admin(user):
    return user.is_staff

@login_required
@user_passes_test(czy_admin)
def panel_administratora(request):
    zgloszenia = Zgloszenie.objects.all().order_by('-data_utworzenia')
    
    wybrany_status = request.GET.get('status', '')
    szukana_fraza = request.GET.get('q', '')
    
    if wybrany_status:
        zgloszenia = zgloszenia.filter(status=wybrany_status)
        
    if szukana_fraza:
        zgloszenia = zgloszenia.filter(
            models.Q(tytul__icontains=szukana_fraza) | 
            models.Q(opis__icontains=szukana_fraza)
        )

    context = {
        'zgloszenia': zgloszenia,
        'wybrany_status': wybrany_status,
        'szukana_fraza': szukana_fraza,
    }
    return render(request, 'zgloszenia/panel_admina.html', context)

@login_required
@user_passes_test(czy_admin)
def zmien_status(request, pk, nowy_status):
    zgloszenie = Zgloszenie.objects.get(pk=pk)
    zgloszenie.status = nowy_status
    zgloszenie.save()
    messages.success(request, f"Status zgłoszenia '{zgloszenie.tytul}' został zmieniony na '{nowy_status}'.")
    return redirect('panel_administratora')

@login_required
def lista_zgloszen(request):
    zgloszenia = Zgloszenie.objects.all().order_by('-data_utworzenia')
    return render(request, 'zgloszenia/lista.html', {'zgloszenia': zgloszenia})

@login_required
def nowe_zgloszenie(request):
    if request.method == "POST":
        form = ZgloszenieForm(request.POST)
        if form.is_valid():
            zgloszenie = form.save(commit=False)
            zgloszenie.autor = User.objects.first() 
            zgloszenie.save()
            messages.success(request, "Zgłoszenie zostało dodane!")
            return redirect('lista_zgloszen')
    else:
        form = ZgloszenieForm()
    
    return render(request, 'zgloszenia/formularz.html', {'form': form})

@login_required
def lista_zgloszen(request):
    zgloszenia = Zgloszenie.objects.filter(autor=request.user).order_by('-data_utworzenia')
    return render(request, 'zgloszenia/lista.html', {'zgloszenia': zgloszenia})

@login_required
def nowe_zgloszenie(request):
    form = ZgloszenieForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        zgloszenie = form.save(commit=False)
        zgloszenie.autor = request.user
        zgloszenie.save()
        return redirect('lista_zgloszen')
    return render(request, 'zgloszenia/formularz.html', {'form': form})

@login_required
def usun_zgloszenie(request, pk):
    zgloszenie = get_object_or_404(Zgloszenie, pk=pk)
    
    if request.user.is_staff or zgloszenie.autor == request.user:
        zgloszenie.delete()
        messages.success(request, "Zgłoszenie zostało pomyślnie usunięte.")
    else:
        messages.error(request, "Nie masz uprawnień do usunięcia tego zgłoszenia!")
    
    if request.user.is_staff:
        return redirect('panel_administratora')
    return redirect('lista_zgloszen')