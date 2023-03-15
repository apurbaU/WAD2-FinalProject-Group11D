from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class Team(models.Model):
    url_slug = models.SlugField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='team_profile_images')
    bio = models.CharField(max_length=4096)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Match(models.Model):
    time = models.DateTimeField()
    
    home_score = models.PositiveSmallIntegerField(null=True)
    away_score = models.PositiveSmallIntegerField(null=True)

    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} @ {self.venue} {self.time}'

class UserProfile(models.Model):
    url_slug = models.SlugField(primary_key=True, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='profile_images', null=True)
    bio = models.CharField(max_length=1024)

    support_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='+')
    work_team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='+')

    def save(self, *args, **kwargs):
        self.url_slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Manager(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    position = models.CharField(max_length=128)

    owned_teams = models.ManyToManyField(Team)

    def __str__(self):
        return self.user.name

class Comment(models.Model):
    body = models.CharField(max_length=4096)
    rating = models.BigIntegerField(default=0)

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    about_match = models.ForeignKey(Match, on_delete=models.CASCADE, null=True)
    replies_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.pk} by {self.user}'
