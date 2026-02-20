from django.contrib import admin
from .models import TaskMetadata

@admin.register(TaskMetadata)
class TaskMetadataAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'task_name', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'task_name')
    search_fields = ('task_id', 'task_name')
    readonly_fields = ('created_at', 'updated_at')
