from django.urls import path
from .views import GlobalDashboardView, WorkshopDashboardView

urlpatterns = [
    path('global/', GlobalDashboardView.as_view(), name='dashboard-global'),
    path('workshop/<int:id>/', WorkshopDashboardView.as_view(), name='dashboard-workshop'),
]
