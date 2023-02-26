from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Initial testing of the site")
