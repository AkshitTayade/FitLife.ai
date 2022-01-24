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

        #return redirect('login_next', user_email_id = user_email_id)

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

def gender(request):
    if request.method == 'POST':
        gender = request.POST['gender']

        if gender == 'male':
            return redirect ('focus_area_male')

        else:
            return redirect('focus_area_female')

    return render(request,'gender.html')

def focus_area_female(request):
    if request.method == 'POST':
        focus_area_female = request.POST['focus_area_female']

        if focus_area_female == 'Arms' or 'Belly' or 'Butt' or 'Legs' or 'FullBody':
            return redirect('personal_details')

        else:
            return redirect('focus_area_female')

    return render(request,'focus-area-female.html')

def focus_area_male(request):
    if request.method == 'POST':
        focus_area_male = request.POST['focus_area_male']

        if focus_area_male == 'Arms' or 'Belly' or 'Butt' or 'Legs' or 'FullBody':
            return redirect('personal_details')

        else:
            return redirect('focus_area_male')

    return render(request,'focus-area-male.html')

def personal_details(request):
    if request.method == 'POST':
        user_name = request.POST['name'].title()
        user_age = request.POST['age']
        user_blood_group = request.POST['bloodgroup']
        print(user_name,user_age,user_blood_group)

        return render(request,'body-details.html',{"user_name": user_name})
        
    return render(request,'personal-details.html')

def body_details(request):
    if request.method == 'POST':
        user_height = request.POST['height']
        user_current_weight = request.POST['current-weight']
        user_targeted_weight = request.POST['targeted-weight']
        print(user_height,user_current_weight,user_targeted_weight)

        #if male redirect to active_status_male
        #else redirect to active_status_female
        

    return render(request,'body-details.html')

def active_status_female(request):
    if request.method == 'POST':
        active_status_female = request.POST['active_status_female']

        if active_status_female == 'option1' or 'option2' or 'option3' or 'option4':
            return redirect('main_goal') 

        else:
            return redirect('active_status_female')    
    
    return render(request,'active-status-female.html')

def active_status_male(request):
    if request.method == 'POST':
        active_status_male = request.POST['active_status_male']

        if active_status_male == 'option1' or 'option2' or 'option3' or 'option4':
            return redirect('main_goal') 

        else:
            return redirect('active_status_male')     
    
    return render(request,'active-status-male.html')

def main_goal(request):
    if request.method == 'POST':
        main_goal = request.POST['main_goal']

        if main_goal == 'EatHealthier' or 'LoseWeight' or 'GainStrength' or 'GetToned' or 'BuildStamina':
            return redirect('dashboard')
        
        else:
            return redirect('main_goal') 

    return render(request,'main-goal.html')



