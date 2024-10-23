# activity_logs/admin.py
from django.contrib import admin
from .models import UserActivityLog

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address', 'user_agent')
    list_filter = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')
    readonly_fields = ('user', 'action', 'timestamp', 'ip_address', 'user_agent', 'extra_data')

    def has_add_permission(self, request):
        # No permitir agregar logs desde el admin manualmente
        return False
