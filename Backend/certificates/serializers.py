from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    workshop_title = serializers.ReadOnlyField(source='registration.workshop.title')
    user_name = serializers.ReadOnlyField(source='registration.user.full_name')

    class Meta:
        model = Certificate
        fields = '__all__'
