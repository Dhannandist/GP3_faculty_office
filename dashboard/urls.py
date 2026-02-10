from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reservasi/', views.reservasi_list, name='reservasi'),
    path('payments/', views.payments, name='payments'),
    path('reports/', views.reports, name='reports'),
    
    # buat laporan bisa jalan
    path('api/report-data/', views.api_report_data, name='api_report_data'),

    #buat checkout nya
    path('checkout/<int:guest_id>/', views.process_checkout, name='process_checkout'),
]