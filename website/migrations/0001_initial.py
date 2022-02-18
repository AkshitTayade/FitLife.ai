# Generated by Django 3.1.7 on 2022-01-26 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_Info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_gender', models.CharField(max_length=50)),
                ('focus_area', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=500)),
                ('user_email', models.CharField(max_length=100)),
                ('user_age', models.IntegerField(default=0)),
                ('user_blood_group', models.CharField(max_length=50)),
                ('user_height', models.IntegerField(default=0)),
                ('user_weight', models.IntegerField(default=0)),
                ('user_activity_level', models.CharField(max_length=100)),
            ],
        ),
    ]