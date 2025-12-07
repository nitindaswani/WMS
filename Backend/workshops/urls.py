from django.urls import path
from .views import WorkshopListCreateView, WorkshopDetailView, SessionListCreateView, SessionDetailView, RegisterUserView, AdminRegisterUserView, AnalyticsView

urlpatterns = [
    path('', WorkshopListCreateView.as_view(), name='workshop-list-create'),
    path('<int:id>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('<int:id>/sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/<int:id>/', SessionDetailView.as_view(), name='session-detail'),
    path('<int:id>/register/<str:user_type>/', RegisterUserView.as_view(), name='workshop-register'),
    path('users/register/', AdminRegisterUserView.as_view(), name='admin-register'), # Alias
    path('admin/register/', AdminRegisterUserView.as_view(), name='admin-register'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
