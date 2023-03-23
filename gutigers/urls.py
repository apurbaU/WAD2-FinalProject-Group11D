from django.urls import path
from gutigers import views
from gutigers.helpers.views import comment

app_name = 'gutigers'

urlpatterns = [
    path('', views.index, name='index'),
    path('404/', views.not_found, name='404'),
    path('settings/', views.settings, name='settings'),
    path('team/<slug:team_name_slug>/', views.team_detail, name='team_detail'),
    path('contact/', views.contact, name='contact'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('result/', views.result, name='result'),
    path('league_table/', views.league_table, name= 'league_table'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('fixtures/save/', views.save_match, name='save_match'),
    path('fixtures/create/', views.create_match, name='create_match'),
    path('user/<slug:username_slug>/', views.user, name='user'),

    # internal pages
    path('comment/<post_id>/new/', comment.comment_new, name='comment_new'),
    path('comment/<int:comment_id>/', comment.comment, name='comment'),
    path('comment/<comment_id>/reply/', comment.comment_reply, name='comment_reply'),
    path('comment/<int:comment_id>/vote/', comment.comment_vote, name='comment_vote'),
]
