from rest_framework import serializers
from .models import USSDUser, USSDSession


class USSDUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for user registration and retrieval.
    '''
    class Meta:
        model = USSDUser
        fields = ['id', 'phone_number', 'language', 'location', 'registered_at']


class USSDSessionSerializer(serializers.ModelSerializer):
    '''
    Serializer for session state tracking.
    '''
    class Meta:
        model = USSDSession
        fields = ['id', 'user', 'session_id', 'last_input', 'is_active', 'created_at', 'updated_at']
