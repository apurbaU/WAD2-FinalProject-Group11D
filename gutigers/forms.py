from django import forms
from gutigers.models import Comment, UserProfile, Team,Match
from django.contrib.auth.models import User
from gutigers.models import Match

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}), help_text='I would like to say:')
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    class Meta:
        model = Comment
        fields = ('body', 'rating')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'display_name', 'support_team')

class SaveMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'venue', 'home_team', 'away_team', 'home_score', 'away_score']
        widgets = {
            'date': forms.DateTimeInput(),
            'home_team': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'away_team': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'home_score': forms.NumberInput(attrs={'min': 0}),
            'away_score': forms.NumberInput(attrs={'min': 0}),
        }

class CreateMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['date', 'venue', 'home_team', 'away_team']
        widgets = {
            'date': forms.DateTimeInput(),
            'home_team': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
            'away_team': forms.Select(attrs={'class': 'selectpicker', 'data-live-search': 'true'}),
        }



class MatchForm(forms.ModelForm):



	class Meta:

		model = Match
		fields = ('date','venue','home_team','away_team','home_score','away_score',)

class ChangeForm(forms.ModelForm):


	class Meta:

		model = UserProfile
		exclude=('url_slug',)

		widgets={'user':forms.HiddenInput(),'work_team':forms.HiddenInput()}
