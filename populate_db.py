#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gutigers_project.settings')

from datetime import date, datetime, timedelta, timezone
import django
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify
from realData import Tigers, Teams

django.setup()
from django.contrib.auth.models import User
from gutigers.models import Comment, Manager, Match, Post, Team, UserProfile

def populate():
<<<<<<< HEAD
    week1=datetime.date(2023, 08, 30)
    t1 = populate_team({'name': Teams.names[0], 'icon': Teams.images[0], 'bio': Teams.bio[0]})
    t2 = populate_team({'name': Teams.names[1], 'icon': Teams.images[1], 'bio': Teams.bio[1]})
    t2 = populate_team({'name': Teams.names[2], 'icon': Teams.images[2], 'bio': Teams.bio[2]})
    t2 = populate_team({'name': Teams.names[3], 'icon': Teams.images[3], 'bio': Teams.bio[3]})
    t2 = populate_team({'name': Teams.names[4], 'icon': Teams.images[4], 'bio': Teams.bio[4]})

    m1 = populate_match({'id': 1, 'date': week1 , 'venue': Team.home[0] 'h_score': 6, 'a_score': 20}, t0, t1)
    m2 = populate_match({'id': 2, 'date': week1+timedelta(days=21) , 'venue': Team.home[4] 'h_score': 6, 'a_score': 6}, t4, t0)
    m3 = populate_match({'id': 3, 'date': week1+timedelta(days=28), 'venue': Team.home[2] 'h_score': 0, 'a_score': 9}, t2, t0)
    m4 = populate_match({'id': 4, 'date': week1+timedelta(days=35), 'venue': Team.home[0] 'h_score': 20, 'a_score': 6}, t1, t0)
    m5 = populate_match({'id': 5, 'date': week1+timedelta(days=49) , 'venue': Team.home[0] 'h_score': 0, 'a_score': 21}, t0, t3)
    m6 = populate_match({'id': 6, 'date': week1+timedelta(days=56) , 'venue': Team.home[0] 'h_score': 0, 'a_score': 0}, t0, t4)
    m7 = populate_match({'id': 7, 'date': week1+timedelta(days=70) , 'venue': Team.home[3] 'h_score': 6, 'a_score': 9}, t3, t0)
    m8 = populate_match({'id': 8, 'date': week1+timedelta(days=77) , 'venue': Team.home[0] 'h_score': 23, 'a_score': 6}, t0, t2)



=======
    t1 = populate_team({'name': 'GUTigers', 'icon': 'team_profile_images/GUTigers.jpg', 'bio': 'Bio of GUTigers'})
    t2 = populate_team({'name': 'Other Team', 'icon': 'profile_images/placeholder.png', 'bio': 'Bio of other team'})
    m1 = populate_match({'id': 1, 'date': datetime.now(timezone.utc), 'venue': 'Football field', 'h_score': 0, 'a_score': 3}, t1, t2)
    m2 = populate_match({'id': 2, 'date': datetime.now(timezone.utc) + timedelta(days=100), 'venue': 'Baseball field', 'h_score': 2, 'a_score': 1}, t2, t1)
>>>>>>> 6855a65b9c722059e70bae032dd5e90cbcdfa444
    u1 = User.objects.get_or_create(username='john@example.org', password='Password1')[0]
    u2 = User.objects.get_or_create(username='connor@example.com', password='12345678')[0]
    up1 = populate_user_profile({'name': 'johnny', 'avatar': 'profile_images/placeholder.png', 'bio': 'John\'s bio', 'support': t1}, u1)
    up2 = populate_user_profile({'name': 'manager', 'avatar': 'team_profile_images/GUTigers.jpg', 'bio': 'Connor\'s bio', 'work': t2}, u2)
    man1 = populate_manager('CEO', up2, [t1, t2])
    p1 = populate_post(1, "Post title", "Post body", date.today())
    c1 = populate_comment({'id': 1, 'body': 'Comment body 1', 'rating': 8627}, up2, p1, None)
    c2 = populate_comment({'id': 2, 'body': 'Comment body 2'}, up1, p1, c1)
    c3 = populate_comment({'id': 3, 'body': 'Comment body 3'}, up2, None, None)

def populate_team(team_spec):
    team = Team.objects.get_or_create(url_slug=slugify(team_spec['name']))[0]
    team.name = team_spec['name']
    team.icon = team_spec['icon']
    team.bio = team_spec['bio']
    team.save()
    return team

def populate_match(match_spec, team1, team2):
    defaults = {'date': datetime.now(timezone.utc), 'home_score': 0, 'away_score': 0, 'home_team': team1, 'away_team': team2}
    match_obj = Match.objects.get_or_create(pk=match_spec['id'], defaults=defaults)[0]
    match_obj.date = match_spec['date']
    match_obj.venue = match_spec['venue']
    match_obj.home_score = match_spec['h_score']
    match_obj.away_score = match_spec['a_score']
    match_obj.home_team = team1
    match_obj.away_team = team2
    match_obj.save()
    return match_obj

def populate_user_profile(profile_spec, user):
    defaults = {'user': user}
    profile = UserProfile.objects.get_or_create(url_slug=slugify(user.username), defaults=defaults)[0]
    profile.display_name = profile_spec['name']
    profile.user = user
    profile.avatar = profile_spec['avatar']
    profile.bio = profile_spec['bio']
    profile.support_team = profile_spec.get('support')
    profile.work_team = profile_spec.get('work')
    profile.save()
    return profile

def populate_manager(position, user, teams):
    manager = Manager.objects.get_or_create(user=user)[0]
    manager.position = position
    manager.save()
    manager.owned_teams.add(*teams)
    return manager

def populate_post(post_id, title, body, post_date):
    defaults = {'post_date': date.today()}
    post = Post.objects.get_or_create(pk=post_id, defaults=defaults)[0]
    post.title = title
    post.body = body
    post.post_date = post_date
    post.save()
    return post

def populate_comment(comment_spec, user, about, replies_to):
    defaults = {'user': user}
    comment = Comment.objects.get_or_create(pk=comment_spec['id'], defaults=defaults)[0]
    comment.body = comment_spec['body']
    comment.rating = comment_spec.setdefault('rating', 0)
    comment.user = user
    comment.about_post = about
    comment.replies_to = replies_to
    comment.save()
    return comment

if __name__ == '__main__':
	populate()
