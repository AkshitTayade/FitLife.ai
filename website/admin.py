# For Superuser :
# python3 manage.py createsuperuser

from django.contrib import admin
from . import models

class User_InfoAdmin(admin.ModelAdmin):
    list_display = ('user_name','user_gender','user_email','user_age','user_blood_group','user_height','user_weight','user_focus_area','user_activity_level')
    list_per_page = 20
    search_fields = ('user_name', 'user_email' ,)

class User_Exercise_InfoAdmin(admin.ModelAdmin):
    list_display = ('user_name','exercise_name' ,'exercise_total_duration','exercise_calorie_burnt')
    list_per_page = 20
    search_fields = ('exercise_name' ,)

class Playlist_Check_InfoAdmin(admin.ModelAdmin):
    list_display = ('user_email','exercise_jj' ,'exercise_ac','exercise_kp', 'exercise_sar', 'exercise_squats', 'exercise_bl', 'exercise_cs')
    list_per_page = 20
    search_fields = ('user_email' ,)


admin.site.register(models.User_Info,User_InfoAdmin)
admin.site.register(models.User_Exercise_Info,User_Exercise_InfoAdmin)
admin.site.register(models.Playlist_Check,Playlist_Check_InfoAdmin)