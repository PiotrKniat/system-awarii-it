from django.shortcuts import render, redirect
from .models import Zgloszenie
from .forms import ZgloszenieForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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