
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gutigers_project.settings')

from datetime import date, datetime, timedelta, timezone
import django
from django.core.files.images import ImageFile
from django.template.defaultfilters import slugify
from realData import Teams

django.setup()
from django.contrib.auth.models import User
from gutigers.models import Comment, Manager, Match, Post, Team, UserProfile

def populate():
    week1=date(2022, 8, 30)
    week9=date(2023, 1, 15)
    t0 = populate_team({'name': Teams.names[0], 'icon': Teams.images[0], 'bio': Teams.bios[0]})
    t1 = populate_team({'name': Teams.names[1], 'icon': Teams.images[1], 'bio': Teams.bios[1]})
    t2 = populate_team({'name': Teams.names[2], 'icon': Teams.images[2], 'bio': Teams.bios[2]})
    t3 = populate_team({'name': Teams.names[3], 'icon': Teams.images[3], 'bio': Teams.bios[3]})
    t4 = populate_team({'name': Teams.names[4], 'icon': Teams.images[4], 'bio': Teams.bios[4]})

    m1 = populate_match({'id': 1, 'date': week1 , 'venue': Teams.home[0], 'h_score': 6, 'a_score': 20}, t0, t1)
    m2 = populate_match({'id': 2, 'date': week1+timedelta(days=21) , 'venue': Teams.home[4], 'h_score': 6, 'a_score': 6}, t4, t0)
    m3 = populate_match({'id': 3, 'date': week1+timedelta(days=28), 'venue': Teams.home[2], 'h_score': 0, 'a_score': 9}, t2, t0)
    m4 = populate_match({'id': 4, 'date': week1+timedelta(days=35), 'venue': Teams.home[1], 'h_score': 20, 'a_score': 6}, t1, t0)
    m5 = populate_match({'id': 5, 'date': week9 , 'venue': Teams.home[0], 'h_score': 21, 'a_score': 0}, t0, t3)
    m6 = populate_match({'id': 6, 'date': week9+timedelta(days=7) , 'venue': Teams.home[0], 'h_score': 0, 'a_score': 0}, t0, t4)
    m7 = populate_match({'id': 7, 'date': week9+timedelta(days=21) , 'venue': Teams.home[3], 'h_score': 6, 'a_score': 9}, t3, t0)
    m8 = populate_match({'id': 8, 'date': week9+timedelta(days=28) , 'venue': Teams.home[0], 'h_score': 23, 'a_score': 6}, t0, t2)

    m9 = populate_match({'id': 9, 'date': week1+timedelta(days=7) , 'venue': Teams.home[1], 'h_score': 28, 'a_score': 10}, t1, t2)
    m10 = populate_match({'id': 10, 'date': week1+timedelta(days=14) , 'venue': Teams.home[4], 'h_score': 0, 'a_score': 28}, t4, t1)
    m11 = populate_match({'id': 11, 'date': week1+timedelta(days=21) , 'venue': Teams.home[1], 'h_score': 48, 'a_score': 0}, t1, t3)
    m12= populate_match({'id': 12, 'date': week9+timedelta(days=14) , 'venue': Teams.home[3], 'h_score': 7, 'a_score': 42}, t3, t1)
    m13= populate_match({'id': 13, 'date': week9+timedelta(days=21) , 'venue': Teams.home[2], 'h_score': 8, 'a_score': 28}, t2, t1)
    m14= populate_match({'id': 14, 'date': week9+timedelta(days=28) , 'venue': Teams.home[1], 'h_score': 55, 'a_score': 0}, t1, t4)

    m15 = populate_match({'id': 15, 'date': week1, 'venue': Teams.home[3], 'h_score': 6, 'a_score': 18}, t3, t2)
    m16= populate_match({'id': 16, 'date': week1+timedelta(days=42), 'venue': Teams.home[2], 'h_score': 6, 'a_score': 14}, t2, t4)
    m17= populate_match({'id': 17, 'date': week9+timedelta(days=7), 'venue': Teams.home[2], 'h_score': 20, 'a_score': 0}, t2, t3)
    m18= populate_match({'id': 18, 'date': week9+timedelta(days=14), 'venue': Teams.home[4], 'h_score': 6, 'a_score': 24}, t4, t2)

    m19= populate_match({'id': 19, 'date': week1+timedelta(days=7), 'venue': Teams.home[4], 'h_score': 6, 'a_score': 8}, t4, t3)
    m20= populate_match({'id': 20, 'date': week1+timedelta(days=42), 'venue': Teams.home[3],'h_score': 20, 'a_score': 15}, t3, t4)

    m8 = populate_match({'id': 21, 'date': datetime.now()+timedelta(days=10, hours=3) , 'venue': Teams.home[4], 'h_score': 0, 'a_score': 0}, t4, t0)
    m8 = populate_match({'id': 22, 'date': datetime.now()+timedelta(days=28, hours=4) , 'venue': Teams.home[2], 'h_score': 0, 'a_score': 0}, t1, t2)
    m8 = populate_match({'id': 23, 'date': datetime.now()+timedelta(days=42, hours=-5) , 'venue': Teams.home[3], 'h_score': 0, 'a_score': 0}, t3, t2)
    m8 = populate_match({'id': 24, 'date': datetime.now()+timedelta(days=63, hours=1) , 'venue': Teams.home[1], 'h_score': 0, 'a_score': 0}, t0, t1)

 


    u1 = User.objects.get_or_create(username='john@example.org', password='Password1')[0]
    u2 = User.objects.get_or_create(username='aidan@example.com', password='12345678')[0]
    u3 = User.objects.get_or_create(username='brian@example.com', password='12345678')[0]
    u4 = User.objects.get_or_create(username='charlie@example.com', password='pbkdf2_sha256$150000$FPTzHLtOQD0L$mZEM/8BomJDL6iY71/gTMtO3rL/phwVJrBj8qIBGye4=')[0]
    up1 = populate_user_profile({'name': 'Johnny', 'avatar': 'profile_images/Johnny.png', 'bio': 'QB for Glasgow Tigers', 'support': t0}, u1)
    up2 = populate_user_profile({'name': 'Aidan', 'avatar': 'profile_images/Aidan.png', 'bio': 'Glasgow Tigers Board members and OL captain', 'support': t0}, u2)
    up3 = populate_user_profile({'name': 'Brian', 'avatar': 'profile_images/Brian.png', 'bio': 'Leeds Gryphons fans studying at GU', 'support': t1}, u3)
    up4 = populate_user_profile({'name': 'Charlie', 'avatar': 'profile_images/GUTigers.jpg', 'bio': "Manager of the GUTigers", 'work': t0}, u4)
    man1 = populate_manager('President', up4, [t0])

    p1 = populate_post(1, "Tigers Lose in Last 16", "On sunday the GUTigers lost in an exciting game away from home against the NTU Renegades 24-9. After a early 2 touchdowns form NTU tigers got their own back and looked to be coming into the game until some poor performances on special teams allowed NTU to return a punt and put the game to bed", date(2023,2,27))
    p2 = populate_post(2, "AGM This Thursday", "This thursday tigers are hosting their AGM at 7pm at The West End Wendy on Byres Road. Its vital that as many club members as possible show up to the meeting to listen to proposed changes. Thanks", date(2023,3,20))
   
    c1 = populate_comment({'id': 1, 'body': 'Good effort from the boys we will get back here next year for sure', 'rating': 87}, up2, p1, None)
    c2 = populate_comment({'id': 2, 'body': 'Too right we can build on this for next year'}, up1, p1, c1)
    c3 = populate_comment({'id': 3, 'body': 'Come On Tigers'}, up2, None, None)
    c4 = populate_comment({'id': 4, 'body': 'Those Coming Reply to this'}, up4, p2, None)
    c6 = populate_comment({'id': 5, 'body': 'Attending'}, up1, p2, c4)
    c5 = populate_comment({'id': 6, 'body': 'Ill be there.'}, up2, p2, c4)
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
