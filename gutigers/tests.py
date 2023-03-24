from django.test import TestCase, Client
from gutigers.models import Match, Team, Post, UserProfile
from gutigers.forms import UserForm, UserProfileForm
from django.utils import timezone
from gutigers.helpers.match import TeamMatchDataView
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth.models import User

# Create your tests here.
class PostTests(TestCase):
    def test_post(self):
        post1 = Post(title='Test', body='testtest', post_date=timezone.now())
        post1.save()
        
        response = self.client.get(reverse('gutigers:post', kwargs={'post_id': post1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gutigers/post.html')
        self.assertContains(response, post1.body)
        
    def test_404_post(self):
        response = self.client.get(reverse('gutigers:post', kwargs={'post_id': 6}))
        self.assertEqual(response.status_code, 302)
    
        
class TeamViewTest(TestCase):
    def test_team_view(self):
        team = Team.objects.create(name='Test Team', url_slug='test-team')
        
        response = self.client.get(reverse('gutigers:team_detail', kwargs={'team_name_slug': team.url_slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gutigers/team.html')
        self.assertEqual(response.context['team'], team)

class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('gutigers:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gutigers/index.html')

class RegisterViewTestCase(TestCase):
    def test_register(self):
        username = "testuser"
        password = "testpassword"
        email = "testuser@example.com"
        first_name = "Test"
        last_name = "User"
        avatar = 'profile_images/placeholder.png'

        expected_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        expected_profile = UserProfile.objects.create(
            user=expected_user,
            avatar=avatar
        )

        response = self.client.post(reverse("gutigers:register"), {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "avatar": avatar,
        })

        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.filter(username=username).count(), 1)
        self.assertEqual(User.objects.filter(username=username).first().email, email)

        self.assertEqual(UserProfile.objects.filter(user=expected_user).count(), 1)
        self.assertEqual(UserProfile.objects.filter(user=expected_user).first().avatar, avatar)

    
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('gutigers:login')
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(self.username, password=self.password)

    def test_login_successful(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('gutigers:index'))
        self.assertTrue(self.client.session['_auth_user_id'] == str(self.user.id))
    
    def test_login_failure(self):
        response = self.client.post(self.url, {'username': self.username, 'password': 'wrongpass'})
        self.assertRedirects(response, reverse('gutigers:login'))

    def test_login_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gutigers/login.html')
        self.assertContains(response, 'Username:')
        self.assertContains(response, 'Password:')
    