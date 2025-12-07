from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import SpeakerProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role', 'phone', 'organization', 'profile_photo')

class SpeakerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakerProfile
        fields = ('bio', 'linkedin', 'expertise', 'photo')

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'role', 'phone')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if validated_data.get('role') == 'speaker':
            SpeakerProfile.objects.create(user=user)
        return user
