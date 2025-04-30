from django.db import models
from django.contrib.auth.models import User
import datetime

class Personel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    izin_gunu = models.FloatField(default=15)

    def __str__(self):
        return f"{self.ad} {self.soyad}"

class GirisCikisKaydi(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE)
    tarih = models.DateField(auto_now_add=True)
    giris_saati = models.TimeField(null=True, blank=True)
    cikis_saati = models.TimeField(null=True, blank=True)

    def gec_kaldi_mi(self):
        if self.giris_saati:
            return self.giris_saati > datetime.time(8, 0)
        return False

    def calisma_suresi(self):
        if self.giris_saati and self.cikis_saati:
            giris = datetime.datetime.combine(self.tarih, self.giris_saati)
            cikis = datetime.datetime.combine(self.tarih, self.cikis_saati)
            return (cikis - giris).total_seconds() / 3600  # saat cinsinden
        return 0

    def __str__(self):
        return f"{self.personel} - {self.tarih}"

class IzinTalebi(models.Model):
    personel = models.ForeignKey(Personel, on_delete=models.CASCADE)
    baslangic_tarihi = models.DateField()
    bitis_tarihi = models.DateField()
    durum = models.CharField(max_length=20, choices=[('Beklemede', 'Beklemede'), ('Onaylandı', 'Onaylandı'),
                                                     ('Reddedildi', 'Reddedildi')], default='Beklemede')
    aciklama = models.TextField(blank=True, null=True)

    def izin_suresi(self):
        return (self.bitis_tarihi - self.baslangic_tarihi).days + 1

    def __str__(self):
        return f"{self.personel} → {self.baslangic_tarihi} - {self.bitis_tarihi} ({self.durum})"
