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

        # stats for geenrating OTP
        otp = hotp.now()
        
        msg_html = render_to_string('otp-email.html', {"otp": otp})

        email = EmailMultiAlternatives(f'Fitlife.ai Account - {otp} is your OTP for secure access', '', settings.EMAIL_HOST_USER, [user_email_id])
        email.attach_alternative(msg_html, "text/html")
        email.send()

        return render(request,'login-next.html',{"user_email_id": user_email_id})

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

def dashboard(request):
    return render(request,'dashboard.html')
