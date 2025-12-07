from django.contrib import admin
from .models import Workshop, Session, WorkshopRating

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'speaker', 'seat_limit')
    inlines = [SessionInline]

admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(Session)
admin.site.register(WorkshopRating)
