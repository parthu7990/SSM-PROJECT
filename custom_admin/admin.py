from django.contrib import admin
from .models import AdminActivity


@admin.register(AdminActivity)
class AdminActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'description', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'description', 'model_name']
    readonly_fields = ['created_at']
