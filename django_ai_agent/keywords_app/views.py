from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Keyword, KeywordSearch, PersonInformation
from .serializers import KeywordSerializer, KeywordSearchSerializer, PersonInformationSerializer

class KeywordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing keywords
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def get_queryset(self):
        # Only return keywords for the current user
        return Keyword.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associate the keyword with the current user
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        keyword = get_object_or_404(Keyword, pk=pk)
        keyword.is_active = not keyword.is_active
        keyword.save()
        return Response({
            'status': 'success',
            'message': f'Keyword {"activated" if keyword.is_active else "deactivated"}'
        })

class KeywordSearchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing keyword search records
    """
    queryset = KeywordSearch.objects.all()
    serializer_class = KeywordSearchSerializer

    def get_queryset(self):
        # Only return searches for the current user's keywords
        return KeywordSearch.objects.filter(keyword__created_by=self.request.user)

class PersonInformationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing person information
    """
    queryset = PersonInformation.objects.all()
    serializer_class = PersonInformationSerializer

    def get_queryset(self):
        # Only return information for the current user's keywords
        return PersonInformation.objects.filter(keyword__created_by=self.request.user)
