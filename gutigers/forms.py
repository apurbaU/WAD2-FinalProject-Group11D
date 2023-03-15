from django import form
from gutigers.models import Comment, UserProfile, Team,Match
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}), help_text='Reply:')
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
    team_supported = forms.ModelChoiceField(queryset=Team.objects.all().order_by('name'))
    class Meta:
        model = UserProfile
        fields = ('avatar', 'display_name', 'team_supported')


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

class UserChangeForm(forms.ModelForm):

	display_name = forms.CharField(max_length=128,label='Display Name',help_text="Enter new display name")
	avatar = forms.ImageField()
	bio = forms.CharField(max_length=128, label="Bio",help_text="Enter new bio")

	class Meta:

		model = Match
		exclude=('url_slug','user',)

