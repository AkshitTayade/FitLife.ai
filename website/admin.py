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

admin.site.register(models.User_Info,User_InfoAdmin)
admin.site.register(models.User_Exercise_Info,User_Exercise_InfoAdmin)
    