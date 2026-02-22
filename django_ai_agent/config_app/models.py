from django.db import models
from django.contrib.auth.models import User

class Platform(models.Model):
    """
    Model to store platform configurations
    """
    name = models.CharField(max_length=100)
    url = models.URLField()
    api_key = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AIModel(models.Model):
    """
    Model to store AI model configurations
    """
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=50, choices=[
        ('openai', 'OpenAI'),
        ('anthropic', 'Anthropic'),
        ('google', 'Google'),
        ('azure', 'Azure'),
        ('mistral', 'Mistral'),
        ('together', 'Together AI'),
        ('ollama', 'Ollama'),
        ('custom', 'Custom')
    ])
    api_key = models.CharField(max_length=255, blank=True, null=True)
    model_name = models.CharField(max_length=100)
    base_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider} - {self.model_name}"

class UserConfiguration(models.Model):
    """
    Model to store user-specific configurations
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_ai_model = models.ForeignKey(AIModel, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuration for {self.user.username}"
