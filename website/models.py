# For Making Migrations of New Database :
        # python3 manage.py makemigrations website
        # python3 manage.py migrate


from django.db import models

# Create your models here.

class User_Info(models.Model):
    user_id = models.AutoField
    user_gender = models.CharField(max_length=50,blank=False,null=False)
    user_focus_area = models.CharField(max_length=100,blank=False,null=False)
    user_name = models.CharField(max_length=500,blank=False,null=False)
    user_email = models.CharField(max_length=100,blank=False,null=False)
    user_age = models.IntegerField(default=0)
    user_blood_group = models.CharField(max_length=50,blank=False,null=False)
    user_height = models.FloatField(default=0)
    user_weight = models.IntegerField(default=0)
    user_activity_level = models.CharField(max_length=100,blank=False,null=False)

    def __str__(self):
        return self.user_email