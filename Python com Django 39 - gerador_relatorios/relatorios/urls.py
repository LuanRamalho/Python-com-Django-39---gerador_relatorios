from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario, name='formulario'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('exportar/excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar/csv/', views.exportar_csv, name='exportar_csv'),
    path('exportar/pdf/', views.exportar_pdf, name='exportar_pdf'),
]
