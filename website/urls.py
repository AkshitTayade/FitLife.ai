from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('login_next', views.login_next, name = 'login_next'), 
    path('resent', views.resend_for_login, name = 'resend_for_login'), 
    path('logout', views.logout_user, name = 'logout_user'), 
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('gender', views.gender, name = 'gender'),
    path('focus_area_female', views.focus_area_female, name = 'focus_area_female'),
    path('focus_area_male', views.focus_area_male, name = 'focus_area_male'),
    path('personal_details', views.personal_details, name = 'personal_details'),
    path('body_details', views.body_details, name = 'body_details'),
    path('active_status_female', views.active_status_female, name = 'active_status_female'),
    path('active_status_male', views.active_status_male, name = 'active_status_male'),
    path('main_goal', views.main_goal, name = 'main_goal'),
    path('exercise/<str:exercise_name>', views.which_exercise, name = 'which_exercise'),
    path('video_feed/<str:exercise_name>', views.video_feed, name='video_feed'),
     path('start_exercise/<str:exercise_name>', views.start_exercise, name='start_exercise'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)