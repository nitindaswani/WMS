from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Workshop, Session
from .serializers import WorkshopSerializer, SessionSerializer
from attendance.models import Registration
from django.contrib.auth import get_user_model
User = get_user_model()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser: # or request.user.role == 'admin'
             return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'role') and request.user.role == 'admin'

class WorkshopListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    
    def get_queryset(self):
        queryset = Workshop.objects.all()
        speaker_id = self.request.query_params.get('speaker_id')
        if speaker_id:
             return queryset.filter(speaker_id=speaker_id)
        
        # Helper for current user
        if self.request.query_params.get('my_workshops') == 'true':
             return queryset.filter(speaker=self.request.user)
             
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class WorkshopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'id'

class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get_queryset(self):
        workshop_id = self.kwargs['id']
        return Session.objects.filter(workshop_id=workshop_id)

    def perform_create(self, serializer):
        workshop = get_object_or_404(Workshop, id=self.kwargs['id'])
        serializer.save(workshop=workshop)

class SessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'id'

class RegisterUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, user_type):
        workshop = get_object_or_404(Workshop, id=id)
        
        # Role Validation
        if user_type == 'student' and request.user.role != 'student' and request.user.role != 'admin':
             return Response({"error": "Only students can register as student"}, status=status.HTTP_403_FORBIDDEN)
        if user_type == 'speaker' and request.user.role != 'speaker' and request.user.role != 'admin':
             return Response({"error": "Only speakers can register as speaker"}, status=status.HTTP_403_FORBIDDEN)
        
        if Registration.objects.filter(user=request.user, workshop=workshop).exists():
             return Response({"error": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)
        
        if workshop.seat_limit > 0 and workshop.registrations.count() >= workshop.seat_limit:
             return Response({"error": "Workshop is full"}, status=status.HTTP_400_BAD_REQUEST)

        reg = Registration.objects.create(user=request.user, workshop=workshop, type=user_type)
        return Response({"message": f"Registered as {user_type} successfully", "registration_id": reg.id}, status=status.HTTP_201_CREATED)

class AdminRegisterUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request):
        workshop_id = request.data.get('workshop_id')
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'student')

        if not workshop_id or not user_id:
             return Response({"error": "workshop_id and user_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        workshop = get_object_or_404(Workshop, id=workshop_id)
        user = get_object_or_404(User, id=user_id)

        if Registration.objects.filter(user=user, workshop=workshop).exists():
             return Response({"error": "User already registered"}, status=status.HTTP_400_BAD_REQUEST)

        Registration.objects.create(user=user, workshop=workshop, type=role)
        return Response({"message": f"User {user.email} registered successfully"}, status=status.HTTP_201_CREATED)

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

class AnalyticsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}
        
        if user.role == 'admin' or user.is_superuser:
            data['total_workshops'] = Workshop.objects.count()
            data['total_participants'] = Registration.objects.count()
            data['budget_utilized'] = Workshop.objects.aggregate(Sum('budget'))['budget__sum'] or 0
            
            # Trends (Last 6 months)
            six_months_ago = timezone.now() - timezone.timedelta(days=180)
            trends = Registration.objects.filter(timestamp__gte=six_months_ago)\
                .annotate(month=TruncMonth('timestamp'))\
                .values('month')\
                .annotate(count=Count('id'))\
                .order_by('month')
            data['trends'] = list(trends) # JSON serializable? month is datetime. Serializer handles it or manual format needed.
            # DRF Response handles datetime usually.
            
            # Upcoming
            upcoming = Workshop.objects.filter(start_date__gte=timezone.now().date()).order_by('start_date')[:5]
            data['upcoming'] = WorkshopSerializer(upcoming, many=True).data
            
        elif user.role == 'speaker':
            data['total_workshops'] = Workshop.objects.filter(speaker=user).count()
            data['total_sessions'] = Session.objects.filter(workshop__speaker=user).count()
            
            # Upcoming sessions where speaker is involved
            upcoming_workshops = Workshop.objects.filter(speaker=user, start_date__gte=timezone.now().date()).order_by('start_date')[:5]
            data['upcoming'] = WorkshopSerializer(upcoming_workshops, many=True).data
            
        elif user.role == 'student':
            data['total_registrations'] = Registration.objects.filter(user=user).count()
            data['certificates'] = 0 # Placeholder until Certificate model exists
            
            # My upcoming
            my_regs = Registration.objects.filter(user=user, workshop__start_date__gte=timezone.now().date()).order_by('workshop__start_date')[:5]
            data['upcoming'] = [reg.workshop.title for reg in my_regs] # Simplified list or full workshop data?
            # Let's return full workshop data for display cards
            workshops = [reg.workshop for reg in my_regs]
            data['upcoming_workshops'] = WorkshopSerializer(workshops, many=True).data

        return Response(data)
