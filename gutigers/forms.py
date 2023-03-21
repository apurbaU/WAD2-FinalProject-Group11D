from django import forms
from gutigers.models import Comment, UserProfile, Team,Match
from django.contrib.auth.models import User


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
        exclude=('url_slug','user')
      


class MatchForm(forms.ModelForm):



	class Meta:

		model = Match
		fields = ('date','venue','home_team','away_team','home_score','away_score',)

class ChangeForm(forms.ModelForm):
	
	
	class Meta:

		model = UserProfile
		exclude=('url_slug',)
		
		widgets={'user':forms.HiddenInput(),'work_team':forms.HiddenInput()}
