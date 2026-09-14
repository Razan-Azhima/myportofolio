from django.contrib import admin
from .models import Experience, Achievement, Education, Skill

# Register your models here.
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'started_at', 'ended_at')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', 'started_at', 'ended_at')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree_or_major', 'faculty', 'period', 'status')
    search_fields = ('institution', 'degree_or_major', 'faculty', 'status')
    list_filter = ('faculty', 'status')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    search_fields = ('name', 'description')
    list_filter = ('category',)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'issuer', 'year')
    search_fields = ('title', 'issuer', 'description')
    list_filter = ('category', 'year')