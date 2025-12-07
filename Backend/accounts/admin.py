from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SpeakerProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'role', 'organization', 'is_staff')
    ordering = ('email',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone', 'organization', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'role', 'phone', 'organization', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SpeakerProfile)
