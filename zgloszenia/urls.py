from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_zgloszen, name='lista_zgloszen'),
    path('nowe/', views.nowe_zgloszenie, name='nowe_zgloszenie'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('zgloszenie/<int:pk>/', views.szczegoly_zgloszenia, name='szczegoly_zgloszenia'),
    path('usun/<int:pk>/', views.usun_zgloszenie, name='usun_zgloszenie'),
    path('zmien-status/<int:pk>/<str:nowy_status>/', views.zmien_status, name='zmien_status'),
    path('panel-it/', views.panel_administratora, name='panel_administratora'),
    path('sprzet/', views.lista_sprzetu, name='lista_sprzetu'),
    path('sprzet/dodaj/', views.dodaj_sprzet, name='dodaj_sprzet'),
    path('sprzet/edytuj/<int:pk>/', views.edytuj_sprzet, name='edytuj_sprzet'),
    path('sprzet/usun/<int:pk>/', views.usun_sprzet, name='usun_sprzet'),
]