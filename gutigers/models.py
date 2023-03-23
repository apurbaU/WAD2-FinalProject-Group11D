from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime


class Team(models.Model):
    url_slug = models.SlugField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='team_profile_images')
    bio = models.CharField(max_length=4096)
    played = models.PositiveIntegerField(default=0)
    won = models.PositiveIntegerField(default=0)
    drawn = models.PositiveIntegerField(default=0)
    lost = models.PositiveIntegerField(default=0)
    goals_for = models.PositiveIntegerField(default=0)
    goals_against = models.PositiveIntegerField(default=0)
    points = models.FloatField(default=0)

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against



    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Match(models.Model):
    date = models.DateTimeField()
    venue = models.CharField(max_length=128)
    home_score = models.PositiveSmallIntegerField(null=True)
    away_score = models.PositiveSmallIntegerField(null=True)
    home_diff_away_score = models.SmallIntegerField(default=0)

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')

    def save(self, *args, **kwargs):
        self.home_diff_away_score = int(self.home_score > self.away_score)
        if self.home_score < self.away_score: self.home_diff_away_score = -1
        super(Match, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.home_team} vs {self.away_team} @ {self.venue} {self.date}'

class UserProfile(models.Model):
    url_slug = models.SlugField(primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='profile_images', null=True, blank=True)
    bio = models.CharField(max_length=1024)

    support_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='+')
    work_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='+')

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.user.username)

        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.display_name

class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    position = models.CharField(max_length=128)

    owned_teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.user.display_name

class Post(models.Model):
    title = models.CharField(max_length=1024)
    body = models.CharField(max_length=16384)
    post_date = models.DateField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    body = models.CharField(max_length=4096)
    rating = models.BigIntegerField(default=0)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    about_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    replies_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.pk} by {self.user}'

class CommentVote(models.Model):
    positive = models.BooleanField()

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{"+1" if self.positive else "-1"} from {self.user} on {self.comment}'
