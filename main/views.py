from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

import datetime

from main.forms import EducationForm, SkillForm, AchievementForm, ExperienceForm
from main.models import Achievement, Education, Experience, Skill

# Create your views here.

# Helper

def is_editor(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="Editor").exists()
    )

# Authentication

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Toggle Star

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    if not is_editor(request.user):
        raise PermissionDenied
    exp = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if exp.starred_by.filter(pk=request.user.pk).exists():
            exp.starred_by.remove(request.user)
        else:
            exp.starred_by.add(request.user)

    return redirect("main:show_experience")

# Show

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Razan Alif Azhima",
        "npm": "2506632942",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "CS student at Universitas Indonesia for longer than planned, now a familiar (and slightly dreaded) face among Fasilkom students as a teaching assistant across several courses"
            # "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

# def show_experience(request):
#     context = {
#         "name": "Razan Alif Azhima",
#         "experience_list": Experience.objects.all(),
#         "is_editor": is_editor(request.user),
#     }
#     return render(request, "experience.html", context)

def show_experience(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Razan Alif Azhima",
        "title_query": title_query,
        "form": ExperienceForm(),
        "is_editor": is_editor(request.user),
    }
    return render(request, "experience.html", context)

def show_achievements(request):
    achievement_list = Achievement.objects.all()
    context = {
        'name': 'Razan Alif Azhima',
        'achievement_list': achievement_list,
    }
    return render(request, 'achievements.html', context)

def show_education(request):
    title_query = request.GET.get("title", "").strip()
    education_list = Education.objects.all()

    if title_query:
        education_list = education_list.filter(institution__icontains=title_query)

    context = {
        "name": "Razan Alif Azhima",
        "education_list": education_list,
        "title_query": title_query,
    }
    return render(request, 'education.html', context)

def show_skills(request):
    skill_list = Skill.objects.all()
    context = {
        'name': 'Razan Alif Azhima',
        'skill_list': skill_list,
    }
    return render(request, 'skills.html', context)

# Create

@require_POST
def create_experience_ajax(request):
    # is_editor() mengecek user: superuser atau anggota group Editor
    if not is_editor(request.user):
        return JsonResponse(
            {"message": "Hanya superuser atau editor yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        exp = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(exp.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
def create_education(request):
    if not is_editor(request.user):
        raise PermissionDenied
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": False,
    }
    return render(request, "education_form.html", context)

@login_required(login_url="/login/")
def create_skill(request):
    if not is_editor(request.user):
        raise PermissionDenied
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": False,
    }
    return render(request, "skill_form.html", context)

@login_required(login_url="/login/")
def create_achievement(request):
    if not is_editor(request.user):
        raise PermissionDenied
    form = AchievementForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Achievement baru berhasil ditambahkan!")
        return redirect("main:show_achievements")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": False,
    }
    return render(request, "achievement_form.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    if not is_editor(request.user):
        raise PermissionDenied
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": False,
    }
    return render(request, "experience_form.html", context)

# Update

@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not is_editor(request.user):
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skills")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": True,
    }
    return render(request, "skill_form.html", context)

@login_required(login_url="/login/")
def update_education(request, education_id):
    if not is_editor(request.user):
        raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(request.POST or None, instance=education)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": True,
    }
    return render(request, "education_form.html", context)

@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not is_editor(request.user):
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Achievement berhasil diperbarui!")
        return redirect("main:show_achievements")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": True,
    }
    return render(request, "achievement_form.html", context)

@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not is_editor(request.user):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
        "is_edit": True,
    }
    return render(request, "experience_form.html", context)

# Delete

@login_required(login_url="/login/")
def delete_education(request, education_id):
    if not is_editor(request.user):
        raise PermissionDenied
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    if not is_editor(request.user):
        raise PermissionDenied
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skills")

    return redirect("main:show_skills")

@login_required(login_url="/login/")
def delete_achievement(request, achievement_id):
    if not is_editor(request.user):
        raise PermissionDenied
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        achievement.delete()
        messages.success(request, "Achievement berhasil dihapus!")
        return redirect("main:show_achievements")

    return redirect("main:show_achievements")

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not is_editor(request.user):
        raise PermissionDenied
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# get JSON 

def get_educations_json(request):
    title_query = request.GET.get("title", "").strip()
    educations = Education.objects.all()

    if title_query:
        educations = educations.filter(institution__icontains=title_query)

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")

def get_achievements_json(request):
    title_query = request.GET.get("title", "").strip()
    achievements = Achievement.objects.all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    achievements_json = serializers.serialize("json", achievements)
    return HttpResponse(achievements_json, content_type="application/json")

def get_skills_json(request):
    name_query = request.GET.get("name", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)

    skills_json = serializers.serialize("json", skills)
    return HttpResponse(skills_json, content_type="application/json")

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for exp in experiences:
        starred_users = exp.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(exp.id),
            "fields": {
                "title": exp.title,
                "description": exp.description,
                "category": exp.category,
                "thumbnail": exp.thumbnail,
                "thumbnail_direct_url": exp.thumbnail_direct_url,
                "started_at": exp.started_at,
                "ended_at": exp.ended_at,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)