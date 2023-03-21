from django.contrib import admin
from gutigers.models import UserProfile, Team, Manager, Match

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Manager)
admin.site.register(Match)