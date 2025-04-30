from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Personel, GirisCikisKaydi
import datetime


def kullanici_giris(request):
    if request.method == 'POST':
        username = request.POST['kullanici_adi']
        password = request.POST['sifre']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('anasayfa')
        else:
            messages.error(request, 'Geçersiz kullanıcı adı ya da şifre')
    return render(request, 'giris.html')


def kullanici_cikis(request):
    logout(request)
    return redirect('giris')


@login_required
def anasayfa(request):
    return render(request, 'anasayfa.html')


@login_required
def giris_yap(request):
    user = request.user
    try:
        personel = Personel.objects.get(user=user)
    except Personel.DoesNotExist:
        return render(request, 'anasayfa.html', {"mesaj": "Bu kullanıcıya ait personel kaydı bulunamadı."})

    bugun = timezone.localdate()
    simdi = timezone.localtime().time()

    kayit, created = GirisCikisKaydi.objects.get_or_create(
        personel=personel,
        tarih=bugun,
    )

    mesaj = ""

    if not kayit.giris_saati:
        kayit.giris_saati = simdi


        gec_kalma_saati = datetime.time(8, 0)
        if simdi > gec_kalma_saati:
            gec_kalma_suresi = (
                datetime.datetime.combine(bugun, simdi) -
                datetime.datetime.combine(bugun, gec_kalma_saati)
            )
            gec_kalma_dakika = gec_kalma_suresi.total_seconds() / 60
            izin_dusulecek = round(gec_kalma_dakika / 60, 2)

            personel.izin_gunu -= izin_dusulecek
            personel.save()

            mesaj = f"Giriş saatiniz kaydedildi. Geç kaldığınız için {izin_dusulecek} gün izninizden düşüldü."
        else:
            mesaj = "Giriş saatiniz kaydedildi."

        kayit.save()

    elif not kayit.cikis_saati:
        kayit.cikis_saati = simdi
        kayit.save()
        mesaj = "Çıkış saatiniz kaydedildi."

    else:
        mesaj = "Bugünkü giriş ve çıkış zaten kaydedilmiş."

    return render(request, 'anasayfa.html', {"mesaj": mesaj})
from .models import IzinTalebi
from django.views.decorators.http import require_POST

@login_required
def izin_talep_et(request):
    if request.method == 'POST':
        baslangic = request.POST['baslangic']
        bitis = request.POST['bitis']
        aciklama = request.POST.get('aciklama', '')

        personel = Personel.objects.get(user=request.user)

        talep = IzinTalebi.objects.create(
            personel=personel,
            baslangic_tarihi=baslangic,
            bitis_tarihi=bitis,
            aciklama=aciklama,
        )
        return render(request, "anasayfa.html", {"mesaj": "İzin talebiniz gönderildi."})

    return render(request, 'izin_talep.html')

@login_required
def izin_taleplerini_gor(request):
    if not request.user.is_staff:
        return redirect('anasayfa')

    talepler = IzinTalebi.objects.all().order_by('-id')
    uyarilacak_personeller = Personel.objects.filter(izin_gunu__lt=3)

    return render(request, 'izin_talepleri.html', {
        "talepler": talepler,
        "uyarilacaklar": uyarilacak_personeller,
    })

@login_required
def izin_talebini_onayla(request, talep_id):
    if not request.user.is_staff:
        return redirect('anasayfa')

    talep = IzinTalebi.objects.get(id=talep_id)
    if talep.durum == 'Beklemede':
        talep.durum = 'Onaylandı'
        talep.save()
        talep.personel.izin_gunu -= talep.izin_suresi()
        talep.personel.save()
    return redirect('izin_talepleri')

@login_required
def izin_talebini_reddet(request, talep_id):
    if not request.user.is_staff:
        return redirect('anasayfa')

    talep = IzinTalebi.objects.get(id=talep_id)
    if talep.durum == 'Beklemede':
        talep.durum = 'Reddedildi'
        talep.save()
    return redirect('izin_talepleri')
from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.db.models.functions import Cast

@login_required
def aylik_rapor(request):
    if not request.user.is_staff:
        return redirect('anasayfa')

    bugun = timezone.now().date()
    baslangic = bugun.replace(day=1)

    kayitlar = (
        GirisCikisKaydi.objects
        .filter(tarih__gte=baslangic, tarih__lte=bugun, giris_saati__isnull=False, cikis_saati__isnull=False)
        .annotate(
            giris_dt=Cast(F('giris_saati'), DurationField()),
            cikis_dt=Cast(F('cikis_saati'), DurationField()),
            fark=ExpressionWrapper(
                Cast(F('cikis_saati'), DurationField()) - Cast(F('giris_saati'), DurationField()),
                output_field=DurationField()
            )
        )
        .values('personel__ad', 'personel__soyad')
        .annotate(toplam_sure=Sum('fark'))
        .order_by('personel__ad')
    )

    return render(request, 'aylik_rapor.html', {'kayitlar': kayitlar, 'ay': bugun.strftime('%B %Y')})



