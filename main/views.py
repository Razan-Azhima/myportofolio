from django.shortcuts import render
from main.models import Experience

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