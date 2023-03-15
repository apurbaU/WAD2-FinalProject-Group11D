from django.urls import path
from gutigers import views

app_name = 'gutigers'

urlpatterns = [
    path('', views.index, name='index'),
    path('team/<slug:team_name_slug>/', views.team_detail, name= 'team_detail'),
    path('contact/', views.contact, name= 'contact'),
    path('player/', views.player, name= 'player'),
    path('post/', views.post, name= 'post'),
    path('login/', views.login, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('result/', views.result, name= 'result'),
    path('user/', views.user, name= 'user'),
    path('settings/', views.settings, name= 'settings'),
 ]
