from rest_framework import serializers
from .models import Workshop, Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = ('workshop',)

class WorkshopSerializer(serializers.ModelSerializer):
    sessions = SessionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Workshop
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at')
