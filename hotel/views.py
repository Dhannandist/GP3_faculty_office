from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Guest, Room


def create_guest(request):
    if request.method == "POST":
        nama = request.POST.get("nama")
        phone = request.POST.get("phone")
        id_card = request.POST.get("id_card_number")
        room_id = request.POST.get("room")

        room = Room.objects.get(id=room_id)

        # VALIDATION: check if room is occupied
        if Guest.objects.filter(room=room, check_out__isnull=True).exists():
            return HttpResponse("Kamar sudah terisi")

        guest = Guest(
            nama=nama,
            phone=phone,
            id_card_number=id_card,
            room=room,
        )

        try:
            guest.full_clean()  # runs model validation
            guest.save()

            # update room status
            room.status = Room.Status.BOOKED
            room.save()

            return HttpResponse("Check-In Berhasil")

        except ValidationError as e:
            return HttpResponse(f"Error: {e}")
