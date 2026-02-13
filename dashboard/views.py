from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django import forms
import datetime

from hotel.models import Guest, Room
from staff.models import StaffModel, UserModel

# utils
from faculty_office.utils.admin_required import admin_required
from faculty_office.utils.login_required import login_required


@login_required
def dashboard(request):
    # Check for user role and redirect them to the correct dashboard view
    if request.user.role == "STAFF":
        return dashboard_staff(request)
    elif request.user.role == "ADMIN":
        # return redirect("dashboard_admin")
        return dashboard_admin(request)
    else:
        messages.error(request, "Login dlu")
        return redirect("login")

    if request.method == "POST":
        nomor_kamar_input = request.POST.get("kamar")
        try:
            kamar_obj = Room.objects.get(room_number=nomor_kamar_input)
            Guest.objects.create(
                nama=request.POST.get("nama_tamu"),
                id_card_number=request.POST.get("no_ktp"),
                phone=request.POST.get("no_hp"),
                room=kamar_obj,
            )
            kamar_obj.status = "booked"
            kamar_obj.save()
            messages.success(request, "Tamu berhasil check-in.")
        except Room.DoesNotExist:
            messages.error(request, "Nomor kamar tidak ditemukan.")
        return redirect("dashboard")

    data_tamu_dashboard = (
        Guest.objects.select_related("room").filter(check_out__isnull=True).order_by("-check_in")[:5]
    )
    context = {
        "total_rooms": Room.objects.count(),
        "available": Room.objects.filter(status="available").count(),
        "occupied": Room.objects.filter(status="booked").count(),
        "reservasi_list": data_tamu_dashboard,
        "rooms": Room.objects.all().order_by("room_number"),
        "intcomma": intcomma,
    }

    messages.success(request, request.user.username)
    messages.success(request, "test msg")
    return render(request, "dashboard.html", context)


@login_required
def dashboard_admin(req):
    if req.method == "POST":
        pass

    data_tamu_dashboard = (
        Guest.objects.select_related("room").filter(check_out__isnull=True).order_by("-check_in")[:5]
    )
    context = {
        "total_rooms": Room.objects.count(),
        "available": Room.objects.filter(status="available").count(),
        "occupied": Room.objects.filter(status="booked").count(),
        "reservasi_list": data_tamu_dashboard,
        "rooms": Room.objects.all().order_by("room_number"),
        "intcomma": intcomma,
    }
    return render(req, "admin/dashboard_admin.html", context)


@login_required
def dashboard_staff(req):
    if req.method == "POST":
        pass

    data_tamu_dashboard = (
        Guest.objects.select_related("room").filter(check_out__isnull=True).order_by("-check_in")[:5]
    )
    context = {
        "total_rooms": Room.objects.count(),
        "available": Room.objects.filter(status="available").count(),
        "occupied": Room.objects.filter(status="booked").count(),
        "reservasi_list": data_tamu_dashboard,
        "rooms": Room.objects.all().order_by("room_number"),
        "intcomma": intcomma,
    }
    return render(req, "dashboard_staff.html", context)


# reservasi list
def reservasi_list(request):
    semua_tamu = Guest.objects.select_related("room").all().order_by("-check_in")
    if request.user.role == "ADMIN":
        html_page = "reservasi_admin.html"
    else:
        html_page = "reservasi_staff.html"

    ### REMOVE FOR PRODUCTION ###
    html_page = "reservasi_staff.html"
    return render(request, html_page, {"data_tamu": semua_tamu})


# payment
def payments(request):
    tamu_lunas = Guest.objects.filter(check_out__isnull=False)
    tamu_nginep = Guest.objects.filter(check_out__isnull=True)

    total_lunas = tamu_lunas.aggregate(Sum("total_price"))["total_price__sum"] or 0

    potensi = 0
    for t in tamu_nginep:
        potensi += t.room.price

    context = {
        "transaksi_list": Guest.objects.all().order_by("-check_in"),
        "total_pendapatan": f"{total_lunas:,}".replace(",", "."),
        "potensi_pendapatan": f"{potensi:,}".replace(",", "."),
    }

    if request.user.role == "ADMIN":
        html_page = "payments_admin.html"
    else:
        html_page = "payments_staff.html"

    ### REMOVE FOR PRODUCTION ###
    html_page = "payments_staff.html"
    return render(request, html_page, context)


# Reports 
def reports(request):
    if request.user.role == "ADMIN":
        html_page = "admin/reports_admin.html"
    else:
        html_page = "reports_staff.html"

    html_page = "reports_staff.html"
    return render(request, html_page)

def process_checkout(request, guest_id):
    # ambil data tamu ID, kalo gak ada return ke 404
    tamu = get_object_or_404(Guest, id=guest_id)

    # ngecek tamu kalo emang belom check-out 
    if not tamu.check_out:
        # set waktu check-out ke waktu sekarang
        tamu.check_out = timezone.now()

        # ngitung durasi nginep (hari)
        # kalo check-in dan check-out di hari yang sama,  ke hitungnya 1 hari
        durasi = (tamu.check_out.date() - tamu.check_in.date()).days
        if durasi < 1:
            durasi = 1
        
        # hitung total tagihannya
        tamu.total_price = durasi * tamu.room.price
        
        # 5. update status kamar jadi 'Available' lagi
        kamar = tamu.room
        kamar.status = 'available'
        kamar.save()

        # simpen perubahan data tamu
        tamu.save()

        messages.success(request, f"Check-out berhasil! Total tagihan: Rp {tamu.total_price:,}")
    
    else:
        messages.warning(request, "Tamu ini sudah melakukan check-out sebelumnya.")

    # kembali ke halaman reservasi
    return redirect('reservasi')

# Admininstration Page
def admininstration(request):
    return render(request, "admin/administrator.html")


# api reports
def api_report_data(request):
    periode = request.GET.get("periode", "daily")
    now = datetime.datetime.now()

    if periode == "daily":
        data = Guest.objects.filter(check_in__date=now.date())
        judul = "PENDAPATAN HARI INI"
    elif periode == "monthly":
        data = Guest.objects.filter(check_in__month=now.month)
        judul = "PENDAPATAN BULAN INI"
    else:
        data = Guest.objects.all()
        judul = "TOTAL PENDAPATAN"

    total = data.aggregate(Sum("total_price"))["total_price__sum"] or 0

    return JsonResponse(
        {
            "judul": judul,
            "total_pendapatan": f"{total:,}".replace(",", "."),
            "total_tamu": data.count(),
        }
    )


@login_required
@admin_required
def manage_staff(req):
    if req.method == "POST":
        if "add_staff" in req.POST:
            staff_form = StaffForm(req.POST)
            if staff_form.is_valid():
                id_user = staff_form.cleaned_data["id_user"]
                staff = StaffModel.objects.create(id_guru=id_user)
                id_user.role = UserModel.UserRoles.GURU
                id_user.save()
                return redirect("administrator")
        elif "edit_staff" in req.POST:
            staff_id = req.POST.get("staff_id")
            staff = StaffModel.objects.get(pk=staff_id)
            user = staff.id

            # Get POST data
            username = req.POST.get("username")
            nama = req.POST.get("nama")
            role = req.POST.get("role")
            is_active = req.POST.get("is_active")
            is_staff = req.POST.get("is_active")
            is_superuser = req.POST.get("is_superuser")
            last_login = req.POST.get("last_login")
            date_joined = req.POST.get("date_joined")

            # Basic validation
            if not username:
                messages.error(req, "Username is required.")
                return redirect("administrator")

            # Check if username is unique (excluding current user)
            if UserModel.objects.filter(username=username).exclude(pk=user.id).exists():
                messages.error(req, "Username is already in use.")
                return redirect("administrator")

            # Update user
            user.username = username
            user.nama = nama
            user.role = role
            user.is_active = is_active
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            # user.
            user.save()

            # Update mapel name
            if nama_mapel:
                mapel = guru.matapelajaranmodel_set.first()
                if mapel:
                    mapel.nama_mapel = nama_mapel
                    mapel.save()

            messages.success(req, "Guru updated successfully!")
            return redirect("manage_guru")
        elif "delete_guru" in req.POST:
            guru_id = req.POST.get("guru_id")
            guru = GuruModel.objects.get(pk=guru_id)
            user = guru.id_guru
            # Delete the user (this will cascade delete the guru due to OneToOneField)
            user.delete()
            messages.success(req, "Guru deleted successfully!")
            return redirect("manage_guru")
    else:
        guru_form = GuruForm()

    guru_list = GuruModel.objects.prefetch_related("matapelajaranmodel_set").all()
    mapel_list = MataPelajaranModel.objects.all()
    context = {"guru_list": guru_list, "mapel_list": mapel_list, "guru_form": guru_form}
    return render(req, "admin/manage_guru.html", context)
