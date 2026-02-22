from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'keywords', views.KeywordViewSet)
router.register(r'searches', views.KeywordSearchViewSet)
router.register(r'person-info', views.PersonInformationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
