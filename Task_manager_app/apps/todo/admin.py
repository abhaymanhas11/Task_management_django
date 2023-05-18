from django.contrib import admin
from apps.todo.models import *


@admin.register(TaskManager)
class Taskadmin(admin.ModelAdmin):
    list_display = ["id", "title", "status", "created_by", "assigned_to"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "task", "body", "created_by"]


@admin.register(Feedback)
class feedbackAdmin(admin.ModelAdmin):
    list_display = ["created_by","task", "rating"]


@admin.register(AddContent)
class ContentAdmin(admin.ModelAdmin):
    list_display = ["created_by", "content", "is_draft"]
