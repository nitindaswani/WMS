from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from attendance.views import UserRegistrationsList
from pathlib import Path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Link directly to the external frontend folder for live updates
# Link directly to the external frontend folder for live updates
FRONTEND_DIR = settings.BASE_DIR.parent / 'Frontend'

urlpatterns = [
    # Renamed Django Admin to avoid conflict with frontend 'admin' folder
    path('django-admin/', admin.site.urls),
    
    # APIs (Auth)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('accounts.urls')),
    path('api/workshops/', include('workshops.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/certificates/', include('certificates.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/user/registrations/', UserRegistrationsList.as_view(), name='user-registrations'),
    
    # Frontend (Serve index.html at root)
    path('', serve, {'document_root': FRONTEND_DIR, 'path': 'frontend/index.html'}),
    
    # Serve all other static files from frontend_host
    re_path(r'^(?P<path>.*)$', serve, {'document_root': FRONTEND_DIR}),
]

# Media URL
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
