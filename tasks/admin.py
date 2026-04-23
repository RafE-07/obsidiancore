from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'importance', 'due_datetime', 'completed', 'created_at']
    list_filter = ['importance', 'completed', 'user']
    search_fields = ['title']
