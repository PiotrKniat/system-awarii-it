from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_zgloszen, name='lista_zgloszen'),
    path('nowe/', views.nowe_zgloszenie, name='nowe_zgloszenie'),
]