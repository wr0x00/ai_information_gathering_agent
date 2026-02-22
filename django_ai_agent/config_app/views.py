from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Platform, AIModel, UserConfiguration
from .serializers import PlatformSerializer, AIModelSerializer, UserConfigurationSerializer

class PlatformViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing platforms
    """
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

    def get_queryset(self):
        # Only return active platforms
        return Platform.objects.filter(is_active=True)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        platform = get_object_or_404(Platform, pk=pk)
        platform.is_active = not platform.is_active
        platform.save()
        return Response({
            'status': 'success',
            'message': f'Platform {"activated" if platform.is_active else "deactivated"}'
        })

class AIModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing AI models
    """
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer

    def get_queryset(self):
        # Only return active AI models
        return AIModel.objects.filter(is_active=True)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        ai_model = get_object_or_404(AIModel, pk=pk)
        ai_model.is_active = not ai_model.is_active
        ai_model.save()
        return Response({
            'status': 'success',
            'message': f'AI Model {"activated" if ai_model.is_active else "deactivated"}'
        })

class UserConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user configurations
    """
    queryset = UserConfiguration.objects.all()
    serializer_class = UserConfigurationSerializer

    def get_queryset(self):
        # Only return configuration for the current user
        return UserConfiguration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associate the configuration with the current user
        serializer.save(user=self.request.user)
