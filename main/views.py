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

def show_skills(request):
    context = {
        "progskill": "Python & Java",
        "progskill_desc": "Pembuatan kode yang komprehensif, cepat dan efisien.",
    }
    return render(request, "skills.html", context)

def show_achievements(request):
    context = {
        "ach1": "Finalis Olimpiade Sains Nasional Astronomi 2024",
    }
    return render(request, "achievements.html", context)

def show_education(request):
    context = {
        "SMA": "SMA Al-Azhar 19 Ciracas",
        "Uni": "Universitas Indonesia",
        "study_prog": "S1 Sistem Informasi",
        "npm": "2506632942",
    }
    return render(request, "education.html", context)