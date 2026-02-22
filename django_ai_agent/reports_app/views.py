from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage
from django.db import models
import os
from .models import Report, ReportTemplate
from .serializers import ReportSerializer, ReportTemplateSerializer

class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing reports
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        # Only return reports for the current user
        return Report.objects.filter(generated_by=self.request.user)

    def perform_create(self, serializer):
        # Associate the report with the current user
        serializer.save(generated_by=self.request.user)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        report = get_object_or_404(Report, pk=pk)
        
        # Check if user has permission to download this report
        if report.generated_by != request.user and not report.is_public:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if file exists
        if not os.path.exists(report.file_path):
            return Response(
                {'error': 'File not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serve the file
        with open(report.file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(report.file_path)}"'
            return response

class ReportTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing report templates
    """
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer

    def get_queryset(self):
        # Only return templates for the current user or active public templates
        return ReportTemplate.objects.filter(
            models.Q(created_by=self.request.user) | 
            models.Q(is_active=True)
        )

    def perform_create(self, serializer):
        # Associate the template with the current user
        serializer.save(created_by=self.request.user)
