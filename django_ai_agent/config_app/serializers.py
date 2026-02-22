from rest_framework import serializers
from .models import Platform, AIModel, UserConfiguration

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class UserConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfiguration
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
