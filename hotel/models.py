from django.db import models
from django.utils import timezone

# kamar hotel
class Room(models.Model):
    
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Tersedia'
        BOOKED = 'booked', 'Terisi'
        UNAVAILABLE = 'unavailable', 'Tidak Tersedia'
    
    room_number = models.CharField(max_length=10, unique=True, verbose_name='Nomor Kamar')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    price = models.IntegerField(verbose_name='Harga per Malam')
    
    class Meta:
        db_table = 'rooms'
        verbose_name = 'Kamar Hotel'
        verbose_name_plural = 'Daftar Kamar'
    
    def __str__(self):
        return f"Kamar {self.room_number} - {self.get_status_display()}"


# data tamu
class Guest(models.Model):
    
    nama = models.CharField(max_length=100, verbose_name='Nama Lengkap')
    phone = models.CharField(max_length=20, verbose_name='No. Telepon')
    id_card_number = models.CharField(max_length=50, verbose_name='NIK/No. Identitas')
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Kamar', db_column='room_id')
    
    check_in = models.DateTimeField(auto_now_add=True, verbose_name='Waktu Check-In')
    check_in_date = models.DateField(auto_now_add=True, verbose_name='Tanggal Check-In')
    
    check_out = models.DateTimeField(null=True, blank=True, verbose_name='Waktu Check-Out')
    check_out_date = models.DateField(null=True, blank=True, verbose_name='Tanggal Check-Out')
    
    total_price = models.IntegerField(default=0, verbose_name='Total Pembayaran')
    
    class Meta:
        db_table = 'guests'
        verbose_name = 'Data Tamu'
        verbose_name_plural = 'Daftar Tamu'
        ordering = ['-check_in']
    
    def __str__(self):
        return f"{self.nama} - Kamar {self.room.room_number}"
    
    # cek udh checkout apa blm
    def is_checked_out(self):
        return self.check_out is not None


# laporan keuangan
class Report(models.Model):
    
    class ReportType(models.TextChoices):
        DAILY = 'daily', 'Laporan Harian'
        MONTHLY = 'monthly', 'Laporan Bulanan'
        GUEST_LIST = 'guest_list', 'Daftar Tamu'
    
    report_type = models.CharField(max_length=20, choices=ReportType.choices, verbose_name='Jenis Laporan')
    
    date_from = models.DateField(verbose_name='Dari Tanggal')
    date_to = models.DateField(verbose_name='Sampai Tanggal')
    
    # FK ke user yg generate
    generated_by = models.ForeignKey('staff.UserModel', on_delete=models.SET_NULL, null=True, verbose_name='Dibuat Oleh', db_column='generated_by_id')
    
    # data finance
    total_revenue = models.IntegerField(default=0, verbose_name='Total Pendapatan (Rp)')
    total_guests = models.IntegerField(default=0, verbose_name='Jumlah Tamu')
    total_rooms_occupied = models.IntegerField(default=0, verbose_name='Kamar Terisi')
    total_record = models.IntegerField(default=0, verbose_name='Jumlah Data')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Dibuat Pada')
    
    class Meta:
        db_table = 'reports'
        verbose_name = 'Laporan'
        verbose_name_plural = 'Daftar Laporan'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.date_from} s/d {self.date_to}"
    
    def format_revenue(self):
        # format ke rupiah
        return f"Rp {self.total_revenue:,}".replace(',', '.')
