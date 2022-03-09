from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login', views.login, name = 'login'),
    path('login_next', views.login_next, name = 'login_next'),
    path('logout', views.logout_user, name = 'logout_user'), 
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('step1', views.gender, name = 'gender'),
    path('step2_f', views.focus_area_female, name = 'focus_area_female'),
    path('step2_m', views.focus_area_male, name = 'focus_area_male'),
    path('step3', views.personal_details, name = 'personal_details'),
    path('step4', views.body_details, name = 'body_details'),
    path('step5_f', views.active_status_female, name = 'active_status_female'),
    path('step5_m', views.active_status_male, name = 'active_status_male'),
    path('step6', views.main_goal, name = 'main_goal'),
    path('exercise/<str:exercise_name>', views.which_exercise, name = 'which_exercise'),
    path('video_feed/<str:exercise_name>', views.video_feed, name='video_feed'),
    path('start_exercise/<str:exercise_name>', views.start_exercise, name='start_exercise'),
    path('end_workout/<str:exercise_name>', views.end_workout, name='end_workout'),
    path('beginner_playlist', views.beginner_playlist, name='beginner_playlist'),
    path('profile', views.profile, name='profile'),
    path('profile_change/<str:editable>', views.profile_change, name='profile_change'),
    path('bmi_bmr_calculation',views.bmi_bmr_calculation,name='bmi_bmr_calculation'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)