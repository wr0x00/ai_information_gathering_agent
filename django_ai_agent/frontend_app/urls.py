from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('scan/', views.scan, name='scan'),
    path('results/', views.results, name='results'),
    path('reports/', views.reports, name='reports'),
    path('config/', views.config, name='config'),
    path('api/scan/', views.api_scan, name='api_scan'),
    path('health/', views.health_check, name='health_check'),
]
