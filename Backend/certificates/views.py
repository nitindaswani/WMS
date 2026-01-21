from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from .models import Certificate
from attendance.models import Registration, Attendance
from .serializers import CertificateSerializer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class UserCertificatesList(generics.ListAPIView):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(registration__user=self.request.user).select_related('registration', 'registration__workshop', 'registration__user')

class GenerateCertificateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, registration_id):
        registration = get_object_or_404(Registration, id=registration_id)
        
        # Validation: User can only generate their own? Or Admin?
        if request.user != registration.user and request.user.role != 'admin':
             return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
             
        # Check Attendance
        if not Attendance.objects.filter(registration=registration, is_present=True).exists():
             return Response({"error": "Cannot generate certificate. Attendance not marked."}, status=status.HTTP_400_BAD_REQUEST)
             
        # Check existing
        if hasattr(registration, 'certificate'):
             return Response(CertificateSerializer(registration.certificate).data, status=status.HTTP_200_OK)

        # Generate PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        p.setFont("Helvetica-Bold", 24)
        p.drawCentredString(width/2, height - 200, "Certificate of Participation")
        
        p.setFont("Helvetica", 18)
        p.drawCentredString(width/2, height - 250, "This certifies that")
        
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width/2, height - 300, registration.user.full_name)
        
        p.setFont("Helvetica", 18)
        p.drawCentredString(width/2, height - 350, "Has successfully attended the workshop")
        
        p.setFont("Helvetica-Bold", 20)
        p.drawCentredString(width/2, height - 400, registration.workshop.title)
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        
        certificate = Certificate.objects.create(registration=registration)
        filename = f"certificate_{registration.id}.pdf"
        certificate.file.save(filename, ContentFile(buffer.getvalue()))
        certificate.save()
        
        return Response(CertificateSerializer(certificate).data, status=status.HTTP_201_CREATED)
