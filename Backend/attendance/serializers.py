from rest_framework import serializers
from .models import Registration, Attendance

class RegistrationSerializer(serializers.ModelSerializer):
    workshop_title = serializers.ReadOnlyField(source='workshop.title')
    user_name = serializers.ReadOnlyField(source='user.full_name')

    class Meta:
        model = Registration
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
