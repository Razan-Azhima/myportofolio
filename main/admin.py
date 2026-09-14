from django.contrib import admin
from .models import Experience

# Register your models here.

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'started_at', 'ended_at', 'is_ongoing')
    list_filter = ('category',)
    search_fields = ('title', 'description')