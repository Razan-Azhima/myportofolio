from django.shortcuts import render
from main.models import Experience, Project

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm

# Create your views here.
def show_main(request):
    context = {
        "name": "Razan Alif Azhima",
        "npm": "2506632942",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "CS student at Universitas Indonesia for longer than planned, now a familiar (and slightly dreaded) face among Fasilkom students as a teaching assistant across several courses"
            # "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Razan",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

from django.shortcuts import render
from .models import Experience, Achievement, Education, Skill

def show_achievements(request):
    achievement_list = Achievement.objects.all()
    context = {
        'name': 'Razan Alif Azhima',
        'achievement_list': achievement_list,
    }
    return render(request, 'achievements.html', context)

def show_education(request):
    education_list = Education.objects.all()
    context = {
        'name': 'Razan Alif Azhima',
        'education_list': education_list,
    }
    return render(request, 'education.html', context)

def show_skills(request):
    skill_list = Skill.objects.all()
    context = {
        'name': 'Razan Alif Azhima',
        'skill_list': skill_list,
    }
    return render(request, 'skills.html', context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    context = {
        "name": "Razan Alif Azhima",
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)
