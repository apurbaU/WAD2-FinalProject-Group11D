from django.contrib import admin
from django.urls import path
from django.urls import include
from gutigers import views
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('gutigers/', include('gutigers.urls')),
    path('admin/', admin.site.urls),
    ]
