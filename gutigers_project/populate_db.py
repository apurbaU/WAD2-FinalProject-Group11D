#!/usr/bin/env python
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gutigers_project.settings')

from datetime import datetime, timedelta, timezone
import django
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify

django.setup()
from django.contrib.auth.models import User
from gutigers.models import Comment, Manager, Match, Team, UserProfile

def populate():
    t1 = populate_team({'name': 'GUTigers', 'icon': 'team_profile_images/GUTigers.jpg', 'bio': 'Bio of GUTigers'})
    t2 = populate_team({'name': 'Other Team', 'icon': 'profile_images/MockUser.png', 'bio': 'Bio of other team'})
    m1 = populate_match({'id': 1, 'time': datetime.now(timezone.utc), 'venue': 'Football field', 'h_score': 0, 'a_score': 3}, t1, t2)
    m2 = populate_match({'id': 2, 'time': datetime.now(timezone.utc) + timedelta(days=100), 'venue': 'Baseball field', 'h_score': 2, 'a_score': 1}, t2, t1)
    u1 = User.objects.get_or_create(username='john smyth', password='Password1')[0]
    u2 = User.objects.get_or_create(username='connor moore', password='12345678')[0]
    up1 = populate_user_profile({'name': u1.username, 'avatar': 'profile_images/MockUser.png', 'bio': 'John\'s bio', 'join': datetime.now(timezone.utc) - timedelta(days=100), 'support': t1}, u1)
    up2 = populate_user_profile({'name': u2.username, 'avatar': 'team_profile_images/GUTigers.jpg', 'bio': 'Connor\'s bio', 'join': datetime.now(timezone.utc) - timedelta(days=200), 'work': t2}, u2)
    man1 = populate_manager('CEO', up2, [t1, t2])
    c1 = populate_comment({'id': 1, 'body': 'Comment body 1', 'rating': 8627}, up2, m1, None)
    c2 = populate_comment({'id': 2, 'body': 'Comment body 2'}, up1, m1, c1)

def populate_team(team_spec):
    team = Team.objects.get_or_create(url_slug=slugify(team_spec['name']))[0]
    team.name = team_spec['name']
    team.icon = team_spec['icon']
    team.bio = team_spec['bio']
    team.save()
    return team

def populate_match(match_spec, team1, team2):
    defaults = {'time': datetime.now(timezone.utc), 'home_score': 0, 'away_score': 0, 'home_team': team1, 'away_team': team2}
    match_obj = Match.objects.get_or_create(match_id=match_spec['id'], defaults=defaults)[0]
    match_obj.time = match_spec['time']
    match_obj.venue = match_spec['venue']
    match_obj.home_score = match_spec['h_score']
    match_obj.away_score = match_spec['a_score']
    match_obj.home_team = team1
    match_obj.away_team = team2
    match_obj.save()
    return match_obj

def populate_user_profile(profile_spec, user):
    defaults = {'user': user, 'join_date': datetime.now(timezone.utc)}
    profile = UserProfile.objects.get_or_create(uid=slugify(profile_spec['name']), defaults=defaults)[0]
    profile.user = user
    profile.name = profile_spec['name']
    profile.avatar = profile_spec['avatar']
    profile.bio = profile_spec['bio']
    profile.join_date = profile_spec['join']
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

def populate_comment(comment_spec, user, about, replies_to):
    defaults = {'user': user}
    comment = Comment.objects.get_or_create(comment_id=comment_spec['id'], defaults=defaults)[0]
    comment.body = comment_spec['body']
    if comment_spec.get('rating') is not None: comment.rating = comment_spec['rating']
    comment.user = user
    comment.about_match = about
    comment.replies_to = replies_to
    comment.save()
    return comment

if __name__ == '__main__':
	populate()
