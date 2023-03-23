from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from gutigers.forms import CommentForm, MatchForm, UserForm, UserProfileForm, ChangeForm, SaveMatchForm, CreateMatchForm
from gutigers.helpers.comment import CommentView
from gutigers.helpers.profile import ProfileView
from gutigers.models import Comment, Manager, Post, Team, UserProfile, Match

def index(request):
    teams = Team.objects.all()
    matches = Match.objects.filter(date__gt=timezone.now()).order_by('date')
    teams = sorted(teams, key=lambda t: (-t.points, -t.goal_difference, -t.goals_for))
    return render(request, 'gutigers/index.html', context= {'upper_half' : True, 'teams': teams, 'matches': matches})

def not_found(request, exception=None):
    return render(request, 'gutigers/404.html')

def team_detail(request, *, team_name_slug):
    try: context_dict = {'team': Team.objects.get(url_slug=team_name_slug)}
    except Team.DoesNotExist: return redirect(reverse('gutigers:404'))
    context_dict['profile'] = ProfileView(context_dict['team'])
    context_dict['supporter_count'] = (UserProfile.objects
                                       .filter(support_team=context_dict['team']).count())
    if team_name_slug == 'gutigers':
        context_dict['posts'] = Post.objects.order_by('-post_date')
        context_dict['post_id'] = -1
        context_dict['comments'] = list(map(CommentView,
                                        Comment.objects.filter(about_post=None, replies_to=None)))
        context_dict['new_right'] = (request.user.is_authenticated and
            Manager.objects.filter(user=UserProfile.objects.get(user=request.user)).exists())
        return render(request, 'gutigers/team.html', context=context_dict)
    else: return render(request, 'gutigers/profile.html', context=context_dict)

def contact(request):
    return render(request, 'gutigers/contact.html')

def post(request, *, post_id):
    try: context_dict = {'post': Post.objects.get(pk=post_id)}
    except Post.DoesNotExist: return redirect(reverse('gutigers:404'))
    return render(request, 'gutigers/post.html', context=context_dict)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('gutigers:index'))
        else:
            messages.error(request,'Username or password not correct!')
            return redirect(reverse('gutigers:login'))

    else:
        form = AuthenticationForm()
    return render(request, 'gutigers/login.html', {'form': form})

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
    try: context_dict = {'profile': ProfileView(UserProfile.objects.get(url_slug=username_slug))}
    except UserProfile.DoesNotExist: return redirect(reverse('gutigers:404'))
    return render(request, 'gutigers/profile.html', context=context_dict)

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
    matches = Match.objects.filter(date__gt=timezone.now()).order_by('date')

    return render(request, 'gutigers/fixtures.html', {'matches': matches})

@login_required
def settings(request):
    username_slug=UserProfile.objects.get(user=request.user).url_slug

    form = MatchForm()

    if request.method == 'POST':
        form = MatchForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect(reverse('gutigers:settings'))
        else:

            print(form.errors)

    profile=UserProfile.objects.get(pk=username_slug)
    image=profile.avatar
    userform= ChangeForm(instance=profile)

    if request.method == 'POST':
        userform = ChangeForm(request.POST,instance=profile)

        if userform.is_valid():

            profilechange=userform.save(commit=False)

            if 'avatar' in request.FILES:
              profilechange.avatar = request.FILES['avatar']

            profilechange.save()

            return redirect(reverse('gutigers:settings'))
        else:

            print(userform.errors)

    context_dict={'form':form,'userform':userform, 'is_manager':Manager.objects.filter(user=profile).exists(), 'image':image, 'profile':profile}
    return render(request, 'gutigers/settings.html', context=context_dict)
