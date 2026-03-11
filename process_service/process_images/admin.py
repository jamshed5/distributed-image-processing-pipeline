# admin.py
from django.contrib import admin
from .models import ProcessedImage

@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ("filename", "created_at")
    search_fields = ("filename",)
    readonly_fields = ("created_at",)