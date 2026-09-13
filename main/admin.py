from django.contrib import admin
from .models import Skill, Experience

@admin.register(Skill)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "id")
    search_fields = ("name",)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "category", "id")
    search_fields = ("title", "description")