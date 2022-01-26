# For Superuser :
# python3 manage.py createsuperuser

from django.contrib import admin
from . import models

class User_InfoAdmin(admin.ModelAdmin):
    list_display = ('user_gender','user_focus_area','user_name','user_email','user_age','user_blood_group','user_height','user_weight','user_activity_level')
    list_per_page = 20
    search_fields = ('user_name', 'user_email' ,)

admin.site.register(models.User_Info,User_InfoAdmin)
    