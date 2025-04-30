"""
URL configuration for attendancetrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from track import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.anasayfa, name='anasayfa'),
    path('giris/', views.kullanici_giris, name='giris'),
    path('cikis/', views.kullanici_cikis, name='cikis'),
    path('giris-yap/', views.giris_yap, name='giris_yap'),
    path('izin-talep/', views.izin_talep_et, name='izin_talep'),
    path('izin-talepleri/', views.izin_taleplerini_gor, name='izin_talepleri'),
    path('izin-onayla/<int:talep_id>/', views.izin_talebini_onayla, name='izin_onayla'),
    path('izin-reddet/<int:talep_id>/', views.izin_talebini_reddet, name='izin_reddet'),  # ← burada VİRGÜL olmalı
    path('aylik-rapor/', views.aylik_rapor, name='aylik_rapor'),
]

