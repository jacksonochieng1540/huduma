from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='analytics_dashboard'),
    path('dashboard/csv/', views.export_csv, name='export_csv'),
    path('dashboard/pdf/', views.export_pdf, name='export_pdf'),
    path('dashboard/excel/', views.export_excel, name='export_excel'),
]
