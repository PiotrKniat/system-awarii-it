from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_zgloszen, name='lista_zgloszen'),
    path('nowe/', views.nowe_zgloszenie, name='nowe_zgloszenie'),
    path('panel-it/', views.panel_administratora, name='panel_administratora'),
    path('status/<int:pk>/<str:nowy_status>/', views.zmien_status, name='zmien_status'),
    path('register/', views.rejestracja, name='rejestracja'),
    path('usun/<int:pk>/', views.usun_zgloszenie, name='usun_zgloszenie'),
]