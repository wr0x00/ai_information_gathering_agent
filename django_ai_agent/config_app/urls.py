from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'platforms', views.PlatformViewSet)
router.register(r'ai-models', views.AIModelViewSet)
router.register(r'user-configs', views.UserConfigurationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
