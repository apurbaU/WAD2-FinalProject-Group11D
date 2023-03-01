from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from gutigers import views


urlpatterns = [
    path('', views.index, name='index'),
    path('gutigers/', include('gutigers.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
