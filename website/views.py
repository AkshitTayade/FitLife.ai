from os import stat
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
import pyotp
import random
import json

hotp = pyotp.HOTP('base32secret3232', digits=4)

def index(request):
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':

        user_email_id = request.POST['user_email']

        # stats for geenrating OTP
        hotp_counter_id = random.randint(0, 10000)
        otp = hotp.at(hotp_counter_id)
        
        dictionary ={
            "otp_counter_id" : hotp_counter_id,
            "otp" : otp,
        }
  
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 4)
        
        # Writing to sample.json
        with open("otp_creds.json", "w") as outfile:
            outfile.write(json_object)

        send_mail(
            'OTP',
            f'Here is your OTP: {otp}.',
            'akshitspam1@gmail.com',
            [user_email_id],
            fail_silently=False,
        )

        return redirect('login_next')

    return render(request,'login.html')

def login_next(request):
    if request.method == 'POST':
        otp1 = request.POST['otp_1']
        otp2 = request.POST['otp_2']
        otp3 = request.POST['otp_3']
        otp4 = request.POST['otp_4']

        user_otp = otp1 + otp2 + otp3 + otp4
        
        # Opening JSON file
        f = open('otp_creds.json',)
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        generated_otp_counter = data['otp_counter_id']

        status = hotp.verify(user_otp, generated_otp_counter)

        if status == True:
            # messages.success(request, "Successfully Logged In")
            return redirect('index')

        else:
            messages.warning(request, "Invalid OTP! Please try again")
            return redirect('login_next')
        
    return render(request,'login-next.html')

