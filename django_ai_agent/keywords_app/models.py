from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
    """
    Model to store keywords for information gathering
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class KeywordSearch(models.Model):
    """
    Model to store keyword search records
    """
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    platform = models.CharField(max_length=100)
    search_query = models.TextField()
    results_count = models.IntegerField(default=0)
    search_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.keyword.name} on {self.platform}"

class PersonInformation(models.Model):
    """
    Model to store information gathered about a person
    """
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=100)
    profile_url = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    collected_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.nickname}) on {self.platform}"
