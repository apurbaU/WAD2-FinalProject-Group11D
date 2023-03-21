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

	time= forms.DateField(help_text="Date of the game (format dd-mm-yyyy)")
	venue=forms.CharField(max_length=128, help_text="Enter Venue of game")
	homeTeam = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'),
			help_text="Home Teams")
	awayTeam = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'),
			help_text="Away Teams")
	homeScore = forms.IntegerField(help_text="Home Score.")
	awayScore = forms.IntegerField(help_text="Away Score.")

	class Meta:

		model = Match
		fields = ('time','venue','homeTeam','awayTeam','homeScore','awayScore',)

class ChangeForm(forms.ModelForm):
	
	
	class Meta:

		model = UserProfile
		exclude=('url_slug',)
		
		widgets={'user':forms.HiddenInput()}
