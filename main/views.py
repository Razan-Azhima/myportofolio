from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import EducationForm
from main.models import Achievement, Education, Experience, Skill

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

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def show_skills(request):
    skill_list = Skill.objects.all()
    context = {
        'name': 'Razan Alif Azhima',
        'skill_list': skill_list,
    }
    return render(request, 'skills.html', context)


def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education baru berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Razan Alif Azhima",
        "form": form,
    }
    return render(request, "education_form.html", context)

def get_educations_json(request):
    title_query = request.GET.get("title", "").strip()
    educations = Education.objects.all()

    if title_query:
        educations = educations.filter(institution__icontains=title_query)

    educations_json = serializers.serialize("json", educations)
    return HttpResponse(educations_json, content_type="application/json")