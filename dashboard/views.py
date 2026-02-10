from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
import datetime

from hotel.models import Guest, Room 


# dashboard
def dashboard(request):
    if request.method == "POST":
        nomor_kamar_input = request.POST.get('kamar')
        try:
            kamar_obj = Room.objects.get(room_number=nomor_kamar_input)
            Guest.objects.create(
                nama=request.POST.get('nama_tamu'),
                id_card_number=request.POST.get('no_ktp'),
                phone=request.POST.get('no_hp'),
                room=kamar_obj
            )
            kamar_obj.status = 'booked'
            kamar_obj.save()
            messages.success(request, "Tamu berhasil check-in.")
        except Room.DoesNotExist:
            messages.error(request, "Nomor kamar tidak ditemukan.")
        return redirect('dashboard')

    data_tamu_dashboard = Guest.objects.select_related('room').all().order_by('-check_in')[:5]
    context = {
        'total_rooms': Room.objects.count(),
        'available': Room.objects.filter(status='available').count(),
        'occupied': Room.objects.filter(status='booked').count(),
        'reservasi_list': data_tamu_dashboard,
        'rooms': Room.objects.all().order_by('room_number'),
        'intcomma': intcomma,
    }
    return render(request, 'dashboard.html', context)

# reservasi list
def reservasi_list(request):
    semua_tamu = Guest.objects.select_related('room').all().order_by('-check_in')
    return render(request, 'reservasi.html', {'data_tamu': semua_tamu})

# buat payment
def payments(request):
    tamu_lunas = Guest.objects.filter(check_out__isnull=False)
    tamu_nginep = Guest.objects.filter(check_out__isnull=True)
    
    total_lunas = tamu_lunas.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    potensi = 0
    for t in tamu_nginep:
        potensi += t.room.price

    context = {
        'transaksi_list': Guest.objects.all().order_by('-check_in'),
        'total_pendapatan': f"{total_lunas:,}".replace(',', '.'),
        'potensi_pendapatan': f"{potensi:,}".replace(',', '.')
    }
    return render(request, 'payments.html', context)

# buat reports
def reports(request):
    return render(request, 'reports.html')

# api reports
def api_report_data(request):
    periode = request.GET.get('periode', 'daily')
    now = datetime.datetime.now()
    
    if periode == 'daily':
        data = Guest.objects.filter(check_in__date=now.date())
        judul = "PENDAPATAN HARI INI"
    elif periode == 'monthly':
        data = Guest.objects.filter(check_in__month=now.month)
        judul = "PENDAPATAN BULAN INI"
    else:
        data = Guest.objects.all()
        judul = "TOTAL PENDAPATAN"

    total = data.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    return JsonResponse({
        'judul': judul,
        'total_pendapatan': f"{total:,}".replace(',', '.'),
        'total_tamu': data.count()
    })