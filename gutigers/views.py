from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from gutigers.forms import UserForm, UserProfileForm, SaveMatchForm, CreateMatchForm
from gutigers.helpers.comment import CommentView
from gutigers.models import Comment, Manager, Post, Team, UserProfile, Match
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import timezone


def index(request):
    teams = Team.objects.all()
    matches = Match.objects.filter(time__gt=timezone.now()).order_by('time')
    teams = sorted(teams, key=lambda t: (-t.points, -t.goal_difference, -t.goals_for))
    return render(request, 'gutigers/index.html', context= {'upper_half' : True, 'teams': teams, 'matches': matches})

def not_found(request, exception=None):
    return render(request, 'gutigers/404.html')

def team_detail(request, *, team_name_slug):
    context_dict = {'post_id': -1, 'comments': list(map(CommentView,
                    Comment.objects.filter(about_post=None, replies_to=None)))}
    try: context_dict['team'] = Team.objects.get(url_slug=team_name_slug)
    except Team.DoesNotExist: return redirect(reverse('gutigers:404'))
    context_dict['new_right'] = (request.user.is_authenticated and
        Manager.objects.filter(user=UserProfile.objects.get(user=request.user)).exists())
    context_dict['supporter_count'] = (UserProfile.objects
                                       .filter(support_team=context_dict['team']).count())
    return render(request, 'gutigers/team.html', context=context_dict)

def contact(request):
    return render(request, 'gutigers/contact.html')

def player(request):
    return render(request, 'gutigers/player.html')

def post(request, *, post_id):
    try: context_dict = {'post': Post.objects.get(pk=post_id)}
    except Post.DoesNotExist: return redirect(reverse('gutigers:404'))
    return render(request, 'gutigers/post.html', context=context_dict)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('gutigers:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'gutigers/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect(reverse('gutigers:index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        print(profile_form.is_valid())

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            else: profile.avatar = 'profile_images/placeholder.png'

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                    'gutigers/register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})

def result(request):
    return render(request, 'gutigers/result.html')

def user(request, *, username_slug):
    return render(request, 'gutigers/user.html')
    
def league_table(request):
    teams = Team.objects.all()
    teams = sorted(teams, key=lambda t: (-t.points, -t.goal_difference, -t.goals_for))
    print(teams)
    return render(request, 'gutigers/league_table.html', {'teams': teams})

def save_match(request):
    form = SaveMatchForm()
    if request.method == 'POST':
        form = SaveMatchForm(request.POST)
        if form.is_valid():
            # Save the form data to a new Match object
            match = form.save()

            # Update the associated Team objects based on the match results
            home_team = match.home_team
            away_team = match.away_team

            home_team.played += 1
            away_team.played += 1

            home_team.goals_for += match.home_score
            home_team.goals_against += match.away_score
            away_team.goals_for += match.away_score
            away_team.goals_against += match.home_score

            if match.home_score > match.away_score:
                home_team.won += 1
                away_team.lost += 1
                home_team.points += 3
            elif match.home_score < match.away_score:
                home_team.lost += 1
                away_team.won += 1
                away_team.points += 3
            else:
                home_team.drawn += 1
                away_team.drawn += 1
                home_team.points += 1
                away_team.points += 1

            home_team.save()
            away_team.save()

            return HttpResponse("Match Saved")
        else:
            print(form)
            teams = Team.objects.all()
            return render(request, 'gutigers/save_match.html', {'teams': teams, 'form':form})
    else:
    # Render the form template
        teams = Team.objects.all()
        return render(request, 'gutigers/save_match.html', {'teams': teams, 'form':form})
        
def create_match(request):
    form = CreateMatchForm()
    if request.method == 'POST':
        form = CreateMatchForm(request.POST)
        if form.is_valid():
            # Save the form data to a new Match object
            match = form.save()

            return redirect(reverse('gutigers:fixtures'))
        else:
            teams = Team.objects.all()
            return render(request, 'gutigers/create_match.html', {'teams': teams, 'form': form})
    else:
        teams = Team.objects.all()
        return render(request, 'gutigers/create_match.html', {'teams': teams, 'form': form})
        
def fixtures(request):
    matches = Match.objects.filter(time__gt=timezone.now()).order_by('time')
    
    return render(request, 'gutigers/fixtures.html', {'matches': matches})