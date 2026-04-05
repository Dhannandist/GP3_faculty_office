from django.contrib import admin
from .models import Room, Guest, Report

# admin utk room
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'status', 'price')
    list_filter = ('status',)
    search_fields = ('room_number',)
    ordering = ('room_number',)
    list_editable = ('status', 'price')

# admin guest
class GuestAdmin(admin.ModelAdmin):
    list_display = ('nama', 'room', 'phone', 'check_in_date', 'check_out_date', 'total_price')
    list_filter = ('check_in_date', 'room')
    search_fields = ('nama', 'phone', 'id_card_number')
    ordering = ('-check_in',)
    readonly_fields = ('check_in', 'check_in_date')
    
    fieldsets = (
        ('Data Tamu', {
            'fields': ('nama', 'phone', 'id_card_number')
        }),
        ('Kamar & Tanggal', {
            'fields': ('room', 'check_in', 'check_in_date', 'check_out', 'check_out_date')
        }),
        ('Pembayaran', {
            'fields': ('total_price',)
        }),
    )

# laporan
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'date_from', 'date_to', 'total_revenue', 'total_guests', 'generated_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('generated_by__nama',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Jenis & Periode', {
            'fields': ('report_type', 'date_from', 'date_to')
        }),
        ('Data Keuangan', {
            'fields': ('total_revenue', 'total_guests', 'total_rooms_occupied', 'total_record')
        }),
        ('Info', {
            'fields': ('generated_by', 'created_at')
        }),
    )


admin.site.register(Room, RoomAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Report, ReportAdmin)
