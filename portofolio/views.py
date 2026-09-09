from django.shortcuts import render
from main.models import Experience


def landing_page(request):
    return render(request, "index.html")