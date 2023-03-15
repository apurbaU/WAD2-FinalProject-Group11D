from http import HTTPStatus
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from gutigers.forms import CommentForm, UserForm, UserProfileForm
from gutigers.helpers.comment import CommentView
from gutigers.models import Comment, Post, Team, User, UserProfile
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login
import sys

def index(request):
    return render(request, 'gutigers/index.html')

def not_found(request):
    return render(request, 'gutigers/404.html')

def comment(request, *, comment_id):
    try: context_dict = {'comment': CommentView(Comment.objects.get(pk=comment_id))}
    except Comment.DoesNotExist: return redirect(reverse('gutigers:404'))
    return render(request, 'gutigers/components/comment.html', context=context_dict)

@login_required
def comment_reply(request, *, comment_id):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = UserProfile.objects.get(user=request.user)
            try: comment.replies_to = Comment.objects.get(pk=comment_id)
            except Comment.DoesNotExist: return HttpResponse(status=HTTPStatus.NOT_FOUND)
            comment.about_post = comment.replies_to.about_post
            comment.save()
            new_url = reverse('gutigers:comment', kwargs={'comment_id': comment.pk})
            return HttpResponse(f'<html><body>{new_url}</body></html>')
        else: print(form.errors)
    context_dict = {'comment_id': comment_id, 'form': form}
    return render(request, 'gutigers/components/reply.html', context=context_dict)

def team_detail(request, *, team_name_slug):
    context_dict = {'comments': list(map(CommentView,
                    Comment.objects.filter(about_post=None, replies_to=None)))}
    try: context_dict['team'] = Team.objects.get(url_slug=team_name_slug)
    except Team.DoesNotExist: redirect(reverse('gutigers:404'))
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
            
            #if 'avatar' in request.FILES:
             #   profile.avatar = request.FILES['avatar']
                
               
            #print(request.FILES, file=sys.stderr)
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
