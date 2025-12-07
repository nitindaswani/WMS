from django.urls import path
from .views import GenerateQRCodeView, MarkAttendanceView, UserAttendanceList

urlpatterns = [
    path('qr/<int:registration_id>/', GenerateQRCodeView.as_view(), name='generate-qr'),
    path('mark/', MarkAttendanceView.as_view(), name='mark-attendance'),
    path('user/', UserAttendanceList.as_view(), name='user-attendance'),
]
