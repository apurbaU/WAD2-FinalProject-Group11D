from django.urls import path
from gutigers import views

app_name = 'gutigers'

urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.not_found, name='404'),
    path('comment/<int:comment_id>/', views.comment, name="comment"),
    path('comment/<int:comment_id>/reply/', views.comment_reply, name="comment_reply"),
    path('team/<slug:team_name_slug>/', views.team_detail, name= 'team_detail'),
    path('contact/', views.contact, name= 'contact'),
    path('player/', views.player, name= 'player'),
    path('post/', views.post, name= 'post'),
    path('login/', views.login, name= 'login'),
    path('register/', views.register, name= 'register'),
    path('result/', views.result, name= 'result'),
    path('user/<slug:username_slug>/', views.user, name= 'user'),
    path('settings/', views.settings, name= 'settings'),
 ]
