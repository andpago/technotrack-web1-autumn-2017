from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def rootView(request):
    return render(request, "core/home.html")