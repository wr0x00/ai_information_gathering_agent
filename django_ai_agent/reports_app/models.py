from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    """
    Model to store generated reports
    """
    REPORT_TYPES = [
        ('scan', 'Scan Report'),
        ('keyword', 'Keyword Analysis Report'),
        ('combined', 'Combined Report'),
    ]
    
    REPORT_FORMATS = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('xlsx', 'Excel Spreadsheet'),
        ('json', 'JSON Data'),
        ('html', 'HTML Report'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    format = models.CharField(max_length=10, choices=REPORT_FORMATS)
    file_path = models.CharField(max_length=500)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(help_text="Size in bytes")
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} ({self.format})"

class ReportTemplate(models.Model):
    """
    Model to store report templates
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    template_content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
