from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, SignupSerializer

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        role = request.data.get('role')
        if role == 'admin':
            return Response({"error": "Admin registration is not allowed."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Security/Role Validation
        request_role = request.data.get('role') # Frontend must send this!
        
        if request_role:
            if request_role == 'admin':
                if user.role != 'admin':
                    return Response({"error": "Unauthorized: You are not an admin."}, status=status.HTTP_401_UNAUTHORIZED)
                # Removed hardcoded email check
            elif request_role == 'speaker' and user.role != 'speaker':
                 return Response({"error": "Unauthorized: You are not a speaker."}, status=status.HTTP_401_UNAUTHORIZED)
            elif request_role == 'student' and user.role != 'student':
                 return Response({"error": "Unauthorized: You are not a student."}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'role': user.role,
            'full_name': user.full_name
        })

class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search')
        role = self.request.query_params.get('role')
        if search:
            queryset = queryset.filter(full_name__icontains=search) | queryset.filter(email__icontains=search)
        if role:
            queryset = queryset.filter(role=role)
        return queryset

class SpeakerListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(role='speaker')
