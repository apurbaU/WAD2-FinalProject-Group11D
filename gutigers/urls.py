from django.urls import path
from gutigers import views
from gutigers.helpers.views import comment

app_name = 'gutigers'

urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.not_found, name='404'),
    path('team/<slug:team_name_slug>/', views.team_detail, name='team_detail'),
    path('contact/', views.contact, name='contact'),
    path('player/', views.player, name='player'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('result/', views.result, name='result'),
    path('user/<slug:username_slug>/', views.user, name='user'),

    # internal pages
    path('comment/<post_id>/new/', comment.comment_new, name='comment_new'),
    path('comment/<int:comment_id>/', comment.comment, name='comment'),
    path('comment/<comment_id>/reply/', comment.comment_reply, name='comment_reply'),
]
