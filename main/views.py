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