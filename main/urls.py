from django.urls import path

from main.views import (show_main, show_experience, show_skills, create_skill, show_achievements, show_education, 
                        create_education, get_educations_json, delete_education,update_education, delete_skill, update_skill)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    path("experience/", show_experience, name="show_experience"),

    path("skills/", show_skills, name="show_skills"),
    path("skills/add", create_skill, name="create_skill"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("skills/<uuid:skill_id>/update/", update_skill, name="update_skill"),

    path("achievements/", show_achievements, name="show_achievements"),


    path("education/", show_education, name="show_education"),
    path("education/add", create_education, name="create_education"),
    path("api/educations/", get_educations_json, name="get_educations_json"),
    path("education/<uuid:education_id>/delete/", delete_education, name="delete_education"),
    path("education/<uuid:education_id>/update/", update_education, name="update_education"),
]