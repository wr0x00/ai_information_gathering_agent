from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reports', views.ReportViewSet)
router.register(r'templates', views.ReportTemplateViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
