from os import stat
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import pyotp
import random
import json
from django.urls import reverse
import datetime

hotp = pyotp.TOTP('base32secret3232', digits=4)

def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':

        user_email_id = request.POST['user_email']

        file = open('saving_mail_ids.txt', 'w')
        file.write(user_email_id)
        file.close()

        # stats for geenrating OTP
        otp = hotp.now()
        
        msg_html = render_to_string('otp-email.html', {"otp": otp})

        email = EmailMultiAlternatives(f'Fitlife.ai Account - {otp} is your OTP for secure access', '', settings.EMAIL_HOST_USER, [user_email_id])
        email.attach_alternative(msg_html, "text/html")
        email.send()

        return render(request,'login-next.html', {"user_email_id": user_email_id})

    return render(request,'login.html')

def login_next(request):
    if request.method == 'POST':
        otp1 = request.POST['otp_1']
        otp2 = request.POST['otp_2']
        otp3 = request.POST['otp_3']
        otp4 = request.POST['otp_4']

        user_otp = otp1 + otp2 + otp3 + otp4
        
        status = hotp.verify(str(user_otp))

        if status == True:
            # messages.success(request, "Successfully Logged In")
            # return HttpResponse('<h1>Successfully Logged In</h1>')
            return redirect('dashboard')

        else:
            messages.warning(request, "Invalid OTP! Please try again")
            return redirect('login_next')
        
    return render(request,'login-next.html')

def resend_for_login(request):

    file = open("saving_mail_ids.txt").read()
    #print(file) 
    
    #stats for geenrating OTP
    otp = hotp.now()

    msg_html = render_to_string('otp-email.html', {"otp": otp})

    email = EmailMultiAlternatives(f'Fitlife.ai Account - {otp} is your OTP for secure access', '', settings.EMAIL_HOST_USER, [file])
    email.attach_alternative(msg_html, "text/html")
    email.send()

    return render(request,'login-next.html', {"user_email_id": file})


# if user already exists:
# redirect to dashboard
# else:
# redirect to onboarding process : gender.html
# if user selects previous buttons update the database

# if gender = Male:
# redirect to focus_area_male  and active_status_male and dashboard_male
# else:
# redirect to focus_area_female and active_status_female and dashboard_female


# for previous button in HTML Template 
# Personal Details : if Male then focus_area_male 
#                    else focus_area_female

# Main Goal : if Male then active_status_male
#             else active_status_female


def dashboard(request):
    return render(request,'dashboard.html')

# stroing all the info about their selected choices in json



def gender(request):
    if request.method == 'POST':
        gender = request.POST['gender']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({"gender": gender})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        if gender == 'male':
            return redirect ('focus_area_male')

        else:
            return redirect('focus_area_female')

    return render(request,'gender.html')

def focus_area_female(request):
    if request.method == 'POST':
        focus_area_female = request.POST['focus_area_female']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({"focus_area": focus_area_female})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        if focus_area_female == 'Arms' or 'Belly' or 'Butt' or 'Legs' or 'FullBody':
            return redirect('personal_details')

        else:
            return redirect('focus_area_female')

    return render(request,'focus-area-female.html')

def focus_area_male(request):
    if request.method == 'POST':
        focus_area_male = request.POST['focus_area_male']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({"focus_area": focus_area_male})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()


        if focus_area_male == 'Arms' or 'Belly' or 'Butt' or 'Legs' or 'FullBody':
            return redirect('personal_details')

        else:
            return redirect('focus_area_male')

    return render(request,'focus-area-male.html')

def personal_details(request):
    if request.method == 'POST':
        user_name = request.POST['name'].title()
        user_email = request.POST['email']
        user_age = request.POST['age']
        user_blood_group = request.POST['bloodgroup']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({   "user_name": user_name,
                                "user_email": user_email,
                                "user_age": user_age,
                                "user_blood_group": user_blood_group,})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        return render(request,'body-details.html',{"user_name": user_name})
        
    return render(request,'personal-details.html')

def body_details(request):
    if request.method == 'POST':
        user_height = request.POST['height']
        user_current_weight = request.POST['current-weight']
        user_targeted_weight = request.POST['targeted-weight']
        print(user_height,user_current_weight,user_targeted_weight)

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({   "user_height": user_height,
                                "user_current_weight": user_current_weight,
                                "user_targeted_weight": user_targeted_weight})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        #if male redirect to active_status_male
        if onboard_data['gender'] == 'male':
            return render(request, 'active-status-male.html', {'user_name': onboard_data['user_name']})
        #else redirect to active_status_female

        else:
            return render(request, 'active-status-female.html', {'user_name': onboard_data['user_name']})

    return render(request,'body-details.html')

def active_status_female(request):
    if request.method == 'POST':
        active_status = request.POST['active_status_female']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({"active_status": active_status})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        if active_status == 'Sedentary' or 'Lightly active' or 'Moderately active' or 'Vigorously active':
            return redirect('main_goal') 

        else:
            return redirect('active_status_female')    
    
    return render(request,'active-status-female.html')


def active_status_male(request):
    if request.method == 'POST':
        active_status = request.POST['active_status_male']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({"active_status": active_status})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        if active_status == 'Sedentary' or 'Lightly active' or 'Moderately active' or 'Vigorously active':
            return redirect('main_goal') 

        else:
            return redirect('active_status_male')    
    
    return render(request,'active-status-male.html')

def main_goal(request):
    if request.method == 'POST':
        main_goal = request.POST['main_goal']

        # updating the onboarding json file
        onboard_file = open('website/onboarding_stat.json', 'r+')
        onboard_data = json.load(onboard_file)
        onboard_data.update({"main_goal": main_goal})
        onboard_file.seek(0)
        json.dump(onboard_data, onboard_file)
        onboard_file.close()

        if main_goal == 'EatHealthier' or 'LoseWeight' or 'GainStrength' or 'GetToned' or 'BuildStamina':
            return redirect('dashboard')
        
        else:
            return redirect('main_goal') 

    return render(request,'main-goal.html')



