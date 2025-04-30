from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('giris/', views.kullanici_giris, name='giris'),
    path('cikis/', views.kullanici_cikis, name='cikis'),
    path('giris-yap/', views.giris_yap, name='giris_yap'),


]
