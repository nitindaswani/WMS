from django.urls import path
from .views import GenerateCertificateView, UserCertificatesList

urlpatterns = [
    path('generate/<int:registration_id>/', GenerateCertificateView.as_view(), name='certificate-generate'),
    path('user/', UserCertificatesList.as_view(), name='user-certificates'),
]
