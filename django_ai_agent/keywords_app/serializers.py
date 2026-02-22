from rest_framework import serializers
from .models import Keyword, KeywordSearch, PersonInformation

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class KeywordSearchSerializer(serializers.ModelSerializer):
    keyword_name = serializers.CharField(source='keyword.name', read_only=True)
    
    class Meta:
        model = KeywordSearch
        fields = '__all__'
        read_only_fields = ('search_date',)

class PersonInformationSerializer(serializers.ModelSerializer):
    keyword_name = serializers.CharField(source='keyword.name', read_only=True)
    
    class Meta:
        model = PersonInformation
        fields = '__all__'
        read_only_fields = ('collected_at', 'last_updated')
