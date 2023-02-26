from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'gutigers/index.html')
    
def team(request):
    return render(request, 'gutigers/team.html')
    
def contact(request):
    return render(request, 'gutigers/contact.html')

def player(request):
    return render(request, 'gutigers/player.html')

def team(request):
    return render(request, 'gutigers/team.html')
    
def post(request):
    return render(request, 'gutigers/post.html')
    
def login(request):
    return render(request, 'gutigers/login.html')
    
def register(request):
    return render(request, 'gutigers/register.html')
    
def result(request):
    return render(request, 'gutigers/result.html')
    
def user(request):
    return render(request, 'gutigers/user.html')