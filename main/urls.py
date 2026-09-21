from django.urls import path

from main.views import (
    show_main, show_experience, show_skills, create_skill, create_experience, show_achievements, show_education, 
    create_education, get_educations_json, delete_education, update_education, delete_skill, 
    update_skill, create_achievement, delete_achievement, update_achievement, delete_experience,
    update_experience, get_achievements_json, get_skills_json, get_experiences_json
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_experience, name="show_experience"),
    path("experience/add", create_experience, name="create_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/update/", update_experience, name="update_experience"),

    path("skills/", show_skills, name="show_skills"),
    path("skills/add", create_skill, name="create_skill"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("skills/<uuid:skill_id>/update/", update_skill, name="update_skill"),

    path("achievements/", show_achievements, name="show_achievements"),
    path("achievements/add", create_achievement, name="create_achievement"),
    path("api/achievements/", get_achievements_json, name="get_achievements_json"),
    path("achievements/<uuid:achievement_id>/delete/", delete_achievement, name="delete_achievement"),
    path("achievements/<uuid:achievement_id>/update/", update_achievement, name="update_achievement"),

    path("education/", show_education, name="show_education"),
    path("education/add", create_education, name="create_education"),
    path("api/educations/", get_educations_json, name="get_educations_json"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("education/<uuid:education_id>/update/", update_education, name="update_education"),
]