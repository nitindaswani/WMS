from django.contrib import admin
from .models import Registration, Attendance

class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'workshop', 'type', 'timestamp')
    inlines = [AttendanceInline]
    list_filter = ('workshop', 'type')
    search_fields = ('user__email', 'user__full_name')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('registration', 'timestamp', 'is_present')
    list_filter = ('is_present', 'registration__workshop')

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Attendance, AttendanceAdmin)
