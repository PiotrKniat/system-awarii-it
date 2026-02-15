from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Zgloszenie, Komentarz, Sprzet
from .forms import KomentarzForm, ZgloszenieForm, SprzetForm, ZgloszenieAssignmentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
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
    wybrany_sla = request.GET.get('sla', '')
    
    if wybrany_status:
        zgloszenia = zgloszenia.filter(status=wybrany_status)
        
    if szukana_fraza:
        zgloszenia = zgloszenia.filter(
            Q(tytul__icontains=szukana_fraza) | 
            Q(opis__icontains=szukana_fraza)
        )
    
    if wybrany_sla == 'breached':
        zgloszenia = [z for z in zgloszenia if z.get_sla_status() == 'breached']
    elif wybrany_sla == 'at_risk':
        zgloszenia = [z for z in zgloszenia if z.get_sla_status() == 'at_risk']
    elif wybrany_sla == 'on_track':
        zgloszenia = [z for z in zgloszenia if z.get_sla_status() == 'on_track']

    context = {
        'zgloszenia': zgloszenia,
        'wybrany_status': wybrany_status,
        'szukana_fraza': szukana_fraza,
        'wybrany_sla': wybrany_sla,
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
@user_passes_test(czy_admin)
def przydziel_zgloszenie(request, pk):
    zgloszenie = get_object_or_404(Zgloszenie, pk=pk)
    
    if request.method == 'POST':
        form = ZgloszenieAssignmentForm(request.POST, instance=zgloszenie)
        if form.is_valid():
            assigned_to = form.cleaned_data.get('assigned_to')
            form.save()
            if assigned_to:
                messages.success(request, f"Zgłoszenie '{zgloszenie.tytul}' przydzielono użytkownikowi {assigned_to.username}.")
            else:
                messages.success(request, f"Usunięto przydzielenie zgłoszenia '{zgloszenie.tytul}'.")
            return redirect('panel_administratora')
    else:
        form = ZgloszenieAssignmentForm(instance=zgloszenie)
    
    return render(request, 'zgloszenia/przydziel.html', {'form': form, 'zgloszenie': zgloszenie})

@login_required
@user_passes_test(czy_admin)
def moje_przydzielone_zgloszenia(request):
    """Wyświetla zgłoszenia przydzielone do aktualnego użytkownika IT"""
    zgloszenia = Zgloszenie.objects.filter(assigned_to=request.user).order_by('-data_utworzenia')
    
    wybrany_status = request.GET.get('status', '')
    szukana_fraza = request.GET.get('q', '')
    wybrany_sla = request.GET.get('sla', '')
    
    if wybrany_status:
        zgloszenia = zgloszenia.filter(status=wybrany_status)
        
    if szukana_fraza:
        zgloszenia = zgloszenia.filter(
            Q(tytul__icontains=szukana_fraza) | 
            Q(opis__icontains=szukana_fraza)
        )
    
    if wybrany_sla == 'breached':
        zgloszenia = [z for z in zgloszenia if z.get_sla_status() == 'breached']
    elif wybrany_sla == 'at_risk':
        zgloszenia = [z for z in zgloszenia if z.get_sla_status() == 'at_risk']
    elif wybrany_sla == 'on_track':
        zgloszenia = [z for z in zgloszenia if z.get_sla_status() == 'on_track']

    context = {
        'zgloszenia': zgloszenia,
        'wybrany_status': wybrany_status,
        'szukana_fraza': szukana_fraza,
        'wybrany_sla': wybrany_sla,
    }
    return render(request, 'zgloszenia/moje_przydzielone.html', context)

@login_required
def lista_zgloszen(request):
    zgloszenia = Zgloszenie.objects.filter(autor=request.user).order_by('-data_utworzenia')
    return render(request, 'zgloszenia/lista.html', {'zgloszenia': zgloszenia})

@login_required
def nowe_zgloszenie(request):
    if request.method == 'POST':
        form = ZgloszenieForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            zgloszenie = form.save(commit=False)
            zgloszenie.autor = request.user
            zgloszenie.save()
            messages.success(request, 'Zgłoszenie zostało wysłane!')
            return redirect('lista_zgloszen')
    else:
        form = ZgloszenieForm(user=request.user)
        
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

@login_required
def szczegoly_zgloszenia(request, pk):
    zgloszenie = get_object_or_404(Zgloszenie, pk=pk)

    if request.user != zgloszenie.autor and not request.user.is_staff:
        return HttpResponseForbidden("Nie masz dostępu do tego zgłoszenia.")

    if request.method == 'POST':
        form = KomentarzForm(request.POST)
        if form.is_valid():
            komentarz = form.save(commit=False)
            komentarz.zgloszenie = zgloszenie
            komentarz.autor = request.user
            komentarz.save()
            messages.success(request, 'Dodano komentarz.')
            return redirect('szczegoly_zgloszenia', pk=pk)
    else:
        form = KomentarzForm()

    return render(request, 'zgloszenia/szczegoly.html', {
        'zgloszenie': zgloszenie,
        'komentarze': zgloszenie.komentarze.all().order_by('data_dodania'),
        'form': form
    })

@staff_member_required
def lista_sprzetu(request):
    sprzety = Sprzet.objects.all()
    return render(request, 'zgloszenia/sprzet_lista.html', {'sprzety': sprzety})

@staff_member_required
def dodaj_sprzet(request):
    if request.method == 'POST':
        form = SprzetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Dodano nowe urządzenie.")
            return redirect('lista_sprzetu')
    else:
        form = SprzetForm()
    return render(request, 'zgloszenia/sprzet_form.html', {'form': form, 'tytul': 'Dodaj Sprzęt'})

@staff_member_required
def edytuj_sprzet(request, pk):
    sprzet = get_object_or_404(Sprzet, pk=pk)
    if request.method == 'POST':
        form = SprzetForm(request.POST, instance=sprzet)
        if form.is_valid():
            form.save()
            messages.success(request, "Zaktualizowano dane urządzenia.")
            return redirect('lista_sprzetu')
    else:
        form = SprzetForm(instance=sprzet)
    return render(request, 'zgloszenia/sprzet_form.html', {'form': form, 'tytul': 'Edytuj Sprzęt'})

@staff_member_required
def usun_sprzet(request, pk):
    sprzet = get_object_or_404(Sprzet, pk=pk)
    sprzet.delete()
    messages.success(request, "Urządzenie zostało usunięte.")
    return redirect('lista_sprzetu')