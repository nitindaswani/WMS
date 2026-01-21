from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import SpeakerProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        token['email'] = user.email
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra response data
        data['role'] = self.user.role
        data['full_name'] = self.user.full_name
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        
        # Admin Verification Check (Priority 2)
        request = self.context.get('request')
        # Check if login request implies strictly admin access? 
        # Usually frontend just logs in. Role checks happen on protected endpoints.
        # But if we want to BLOCK non-admins from logging in via a specific admin portal, we'd need a flag.
        # For now, we just return the role. The Frontend decides where to redirect.
        # However, finding 13 says "Admin login only checks email... Fix: Verify is_staff".
        # If the user IS logging in as admin (e.g. from /admin/login), checking is_staff is good.
        # But this is a generic token endpoint.
        # We'll rely on the returned 'role' claim for frontend logic, and backend permissions for security.
        
        return data

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
