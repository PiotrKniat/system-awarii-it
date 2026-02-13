from django.shortcuts import render, redirect, get_object_, some_shortcut
from .models import Zgloszenie
from .forms import ZgloszenieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test

def czy_admin(user):
    return user.is_staff

@login_required
@user_passes_test(czy_admin)
def panel_administratora(request):
    wszystkie_zgloszenia = Zgloszenie.objects.all().order_by('-data_utworzenia')
    
    query = request.GET.get('q')
    if query:
        wszystkie_zgloszenia = wszystkie_zgloszenia.filter(tytul__icontains=query)

    return render(request, 'zgloszenia/panel_admina.html',{
        'zgloszenia': wszystkie_zgloszenia
    })

@login_required
@user_passes_test(czy_admin)
def zmien_status(request, pk, nowy_status):
    # Pobieramy konkretne zgłoszenie po jego ID (pk)
    zgloszenie = Zgloszenie.objects.get(pk=pk)
    zgloszenie.status = nowy_status
    zgloszenie.save()
    return redirect('panel_administratora')

def lista_zgloszen(request):
    zgloszenia = Zgloszenie.objects.all().order_by('-data_utworzenia')
    return render(request, 'zgloszenia/lista.html', {'zgloszenia': zgloszenia})

def nowe_zgloszenie(request):
    if request.method == "POST":
        form = ZgloszenieForm(request.POST)
        if form.is_valid():
            zgloszenie = form.save(commit=False)
            zgloszenie.autor = User.objects.first() 
            zgloszenie.save()
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