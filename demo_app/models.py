from django.db import models

class TaskMetadata(models.Model):
    task_id = models.CharField(max_length=255, unique=True, verbose_name="Task ID")
    task_name = models.CharField(max_length=255, verbose_name="Task Name")
    status = models.CharField(max_length=50, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    result = models.JSONField(null=True, blank=True, verbose_name="Result")

    def __str__(self):
        return f"{self.task_name} ({self.task_id}) - {self.status}"

    class Meta:
        verbose_name = "Task Metadata"
        verbose_name_plural = "Tasks Metadata"
