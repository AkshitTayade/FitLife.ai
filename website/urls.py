from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('login_next', views.login_next, name = 'login_next'), 
    path('dashboard', views.dashboard, name = 'dashboard'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)