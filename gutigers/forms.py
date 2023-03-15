from django import forms
from gutigers.models import Match

class MatchForm(forms.ModelForm):

	time= forms.DateField(help_text="Enter the Date of the game (format dd-mm-yyyy)")
	homeTeam = forms.CharField(max_length=128,
			help_text="Please enter the Home Teams name.")
	awayTeam = forms.CharField(max_length=128,
			help_text="Please enter the Away Teams name.")
	homeScore = forms.IntegerField(help_text="Please enter the Home Score.")
	awayScore = forms.IntegerField(help_text="Please enter the Away Score.")



	class Meta:


		model = Match
		fields = ('time','homeTeam','awayTeam','homeScore','awayScore',)

class UserForm(forms.ModelForm):

	display_name = forms.CharField(max_length=128,label='Display Name',help_text="Enter new display name")
	avatar = forms.ImageField()
	bio = forms.CharField(max_length=128, label="Bio",help_text="Enter new bio")

	class Meta:


		model = Match
		exclude=('url_slug','user',)