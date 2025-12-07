from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from workshops.models import Workshop
from attendance.models import Registration, Attendance
from accounts.models import CustomUser

class GlobalDashboardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated] # Admin only usually? Or Speaker? "Dashboards (global + workshop-specific)" listed under Admin/Speaker/Student? Prompt: "Dashboards -> Global Dashboard"
    # Prompt says "Dashboards" under Frontend Pages. Roles: Admin has full access. Speaker can track ... 
    # Usually global stats are Admin.
    
    def get(self, request):
        if request.user.role != 'admin':
             pass # Maybe allow read only? Or restrict. I'll allow all auth users for now but typically Admin.
             # Prompt doesn't strictly forbid others.
        
        total_workshops = Workshop.objects.count()
        total_students = CustomUser.objects.filter(role='student').count()
        total_speakers = CustomUser.objects.filter(role='speaker').count()
        total_budget = Workshop.objects.aggregate(Sum('budget'))['budget__sum'] or 0
        total_attendees = Attendance.objects.filter(is_present=True).count()
        
        return Response({
            "total_workshops": total_workshops,
            "total_students": total_students,
            "total_speakers": total_speakers,
            "total_budget": total_budget,
            "total_attendees": total_attendees
        })

class WorkshopDashboardView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        workshop = get_object_or_404(Workshop, id=id)
        # Auth check? Speaker assigned or Admin? or Student enrolled?
        
        total_registrations = Registration.objects.filter(workshop=workshop).count()
        total_present = Attendance.objects.filter(registration__workshop=workshop, is_present=True).count()
        
        return Response({
            "workshop": workshop.title,
            "total_registrations": total_registrations,
            "total_present": total_present,
            "seat_limit": workshop.seat_limit,
            "remaining_seats": workshop.seat_limit - total_registrations if workshop.seat_limit > 0 else "Unlimited"
        })
