from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Staff
    path("reservasi/", views.reservasi_list, name="reservasi"),
    path("reservasi/delete/<int:guest_id>/", views.delete_reservation, name="delete_reservation"),
    path("payments/", views.payments, name="payments"),
    path("reports/", views.reports, name="reports"),
    path("administration/", views.admininstration, name="admininstration"),
    # buat laporan bisa jalan
    path("api/report-data/", views.api_report_data, name="api_report_data"),
    path("checkout/<int:guest_id>/", views.process_checkout, name="process_checkout"),
]
