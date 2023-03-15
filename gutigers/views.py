from django.shortcuts import render
from django.http import HttpResponse
from gutigers.models import Team
from gutigers.forms import MatchForm, UserForm

def index(request):
    return render(request, 'gutigers/index.html')

def team_detail(request, *, team_name_slug):
    context_dict = {}
    try: context_dict['team'] = Team.objects.get(url_slug=team_name_slug)
    except Team.DoesNotExist: context_dict['team'] = None
    return render(request, 'gutigers/team.html', context=context_dict)

def contact(request):
    return render(request, 'gutigers/contact.html')

def player(request):
    return render(request, 'gutigers/player.html')

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

def settings(request):
   
    form = MatchForm()

    if request.method == 'POST':
        form = MatchForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect('/gutigers/')
        else:

            print(form.errors)

        form = MatchForm()

    
    form2= UserForm()

    if request.method == 'POST':
        form2 = UserForm(request.POST)

        if form2.is_valid():

            form.save(commit=True)

            return redirect('/gutigers/')
        else:

            print(form2.errors)

    context_dict={'form2':form2}
    return render(request, 'gutigers/settings.html', context=context_dict)

