from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core import signing
from .models import Registration, Attendance
from workshops.models import Session
from .serializers import AttendanceSerializer, RegistrationSerializer
import qrcode
from io import BytesIO

class UserRegistrationsList(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

class UserAttendanceList(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Attendance.objects.filter(registration__user=self.request.user)

class GenerateQRCodeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, registration_id):
        # Allow user to view their own QR, or Admin
        registration = get_object_or_404(Registration, id=registration_id)
        if request.user != registration.user and request.user.role != 'admin':
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        # Crypto token
        import time
        payload = {
            'registration_id': registration.id,
            'user_id': registration.user.id,
            'workshop_id': registration.workshop.id,
            'timestamp': int(time.time())
        }
        token = signing.dumps(payload)
        
        # Generate QR
        img = qrcode.make(token)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        
        return HttpResponse(buffer.getvalue(), content_type="image/png")

class MarkAttendanceView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Admin only?
    
    def post(self, request):
        if request.user.role != 'admin':
             return Response({"error": "Only admin can mark attendance"}, status=status.HTTP_403_FORBIDDEN)
        
        qr_content = request.data.get('qr_content')
        if not qr_content:
            return Response({"error": "qr_content required"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            data = signing.loads(qr_content, max_age=86400) # 1 day validity?
            registration_id = data.get('registration_id')
        except signing.BadSignature:
            return Response({"error": "Invalid QR Code"}, status=status.HTTP_400_BAD_REQUEST)
        
        registration = get_object_or_404(Registration, id=registration_id)
        
        # Check for Session Specific Attendance
        session_id = request.data.get('session_id')
        session = None
        if session_id:
             session = get_object_or_404(Session, id=session_id)
             if session.workshop != registration.workshop:
                  return Response({"error": "Session does not belong to the registered workshop"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if already attended
        # If session is provided, check for that session. If not, check global workshop attendance?
        # Let's assume: if session is provided, it's session attendance. If not, it's workshop attendance (or daily check-in).
        # We'll support both.
        
        query = Attendance.objects.filter(registration=registration)
        if session:
             query = query.filter(session=session)
        else:
             query = query.filter(session__isnull=True)

        if query.exists():
             return Response({"error": "Already marked present"}, status=status.HTTP_400_BAD_REQUEST)
             
        attendance = Attendance.objects.create(
            registration=registration,
            session=session,
            qr_secret=qr_content,
            is_present=True
        )
        
        return Response(AttendanceSerializer(attendance).data, status=status.HTTP_201_CREATED)
