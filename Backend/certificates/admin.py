from django.contrib import admin
from .models import Certificate

class CertificateAdmin(admin.ModelAdmin):
    list_display = ('registration', 'certificate_id', 'issue_date')

admin.site.register(Certificate, CertificateAdmin)
