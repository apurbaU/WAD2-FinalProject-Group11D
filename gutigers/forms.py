from django import forms
from gutigers.models import Comment, UserProfile
from django.contrib.auth.models import User
from gutigers.models import Team

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}), help_text='Reply:')
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Comment
        fields = ('body', 'rating')
      
TEAM_CHOICES = list(map(lambda team: (team.pk, team.name), Team.objects.all()))
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    team_supported = forms.MultipleChoiceField(choices = TEAM_CHOICES)
    class Meta:
        model = UserProfile
        fields = ('avatar', 'display_name', 'team_supported')
