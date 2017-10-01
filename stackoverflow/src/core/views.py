from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def rootView(request):
    return HttpResponse("Hello, welcome to the main page")