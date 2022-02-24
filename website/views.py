from os import stat
from cv2 import RQDecomp3x3
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from numpy import round_
from .models import User_Info,User_Exercise_Info,Playlist_Check
from django.contrib.auth import authenticate, login, logout
import pyotp
import random
import json
import datetime
import cv2 
from django.http.response import StreamingHttpResponse
import time
from .camera import VideoCamera
from .cal_calories_burned import CalorieBurned

hotp = pyotp.HOTP('base32secret3232', digits=4)

def index(request):

    return render(request,'index.html')

def login(request):
    if request.method == 'POST':

        user_email_id = request.POST['user_email']

        existing_user_email_id = User_Info.objects.filter(user_email=user_email_id)

        print(existing_user_email_id)

        if len(existing_user_email_id) > 0:
            
            file = open('saving_mail_ids.txt', 'w')
            file.write(user_email_id)
            file.close()

            # stats for geenrating OTP
            counter_HOTP = random.randint(0, 1000)
            otp = hotp.at(counter_HOTP)

            file = open('website/otp_generation.json', 'r+')
            data = json.load(file)
            data.update({"counter": counter_HOTP, "otp": otp})
            file.seek(0)
            json.dump(data, file)
            file.close()
            
            msg_html = render_to_string('otp-email.html', {"otp": otp})

            email = EmailMultiAlternatives(f'Fitlife.ai Account - {otp} is your OTP for secure access', '', settings.EMAIL_HOST_USER, [user_email_id])
            email.attach_alternative(msg_html, "text/html")
            email.send()

            return render(request,'login-next.html', {"user_email_id": user_email_id})

        else:
            messages.error(request, "Please Register Yourself ! ")
            return redirect('login')


    return render(request,'login.html')

def login_next(request):
    if request.method == 'POST':
        otp1 = request.POST['otp_1']
        otp2 = request.POST['otp_2']
        otp3 = request.POST['otp_3']
        otp4 = request.POST['otp_4']

        user_otp = otp1 + otp2 + otp3 + otp4
        
        file = open('website/otp_generation.json', 'r+')
        data = json.load(file)

        status = hotp.verify(str(user_otp), data['counter'])

        file.close()
        
        if status == True:
            file = open('saving_mail_ids.txt').read()
            request.session['user_mail_id'] =  file
            request.session.modified = True

            user_data = User_Info.objects.filter(user_email=file).first()

            #request.session['user_weight'] = user_data.user_weight

            #print(request.session['user_mail_id'])

            # for refreshing the playlist model daily
            try:
                today_date = datetime.date.today()

                playlist = Playlist_Check.objects.get(user_email =  request.session['user_mail_id'])

                if playlist.current_date < today_date:
                    # refresh the database
                    playlist.exercise_squats = 0
                    playlist.exercise_jj = 0
                    playlist.exercise_ac=0
                    playlist.exercise_kp=0
                    playlist.exercise_squats=0
                    playlist.exercise_bl=0
                    playlist.exercise_cs=0
                    playlist.save()
            
            except:
                pass
            
            return redirect('dashboard')

        else:
            messages.error(request, "Invalid OTP! Please try again")
            
            return redirect('login_next')
        
    return render(request,'login-next.html')

def logout_user(request):
    
    request.session['user_mail_id'] = False
    request.session.modified = True

    print(request.session['user_mail_id'])

    file = open('saving_mail_ids.txt', 'w')
    file.write("")
    file.close()

    return redirect('index')

def dashboard(request):

    if request.session['user_mail_id'] == False:
        return redirect('index')

    else:
        user_playlist = Playlist_Check.objects.filter(user_email=request.session['user_mail_id']).first()
        user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()
        
        return render(request,'dashboard.html',{'user_data': user_data, 'playlist': user_playlist})
          
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
        user_height_ft = int(request.POST['height'])
        user_height_in = int(request.POST['height1'])
        user_height = str(round(((user_height_in/12) + user_height_ft)*30.48, 2))
        user_current_weight = request.POST['current-weight']
        user_targeted_weight = request.POST['targeted-weight']
    
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
            
            # adding the details to the database
            new_user_entry = User_Info(user_gender = onboard_data['gender'],
                                        user_focus_area = onboard_data['focus_area'],
                                        user_name = onboard_data['user_name'],
                                        user_email = onboard_data['user_email'],
                                        user_age = onboard_data['user_age'],
                                        user_blood_group = onboard_data['user_blood_group'],
                                        user_height  = onboard_data['user_height'],
                                        user_weight = onboard_data['user_current_weight'],
                                        user_activity_level = onboard_data['active_status'])

            new_user_entry.save()

            onboard_file = open('website/onboarding_stat.json', 'w')
            json.dump({}, onboard_file)
            onboard_file.close()
            
            # user main goal not there in database
            # user targeted weight not there in database
            messages.info(request, "You have successfully registered ! Now enter your email id and login to the dashboard. ")
            return redirect('login')
        
        else:
            return redirect('main_goal') 

    return render(request,'main-goal.html')

def which_exercise(request, exercise_name):
    
    file = open('website/exercise_timing.json', 'r+')
    data = json.load(file)
    file.close()

    file = open('website/exercise_timing.json', 'w+')
    json.dump({}, file)
    file.close()

    if exercise_name == 'squat': 
        return render(request,'exercises/exercise_squats.html', {"ex_name": exercise_name})

    elif exercise_name == 'jumping jack':
        return render(request,'exercises/exercise_jumping_jack.html', {"ex_name": exercise_name})

    elif exercise_name == 'adbominal crunches':
        return render(request,'exercises/exercise_abdominal_crunches.html', {"ex_name": exercise_name})

    elif exercise_name == 'knee pushup':
        return render(request,'exercises/exercise_knee_pushup.html', {"ex_name": exercise_name})

    elif exercise_name == 'side arm raises':
        return render(request,'exercises/exercise_side_arm_raises.html', {"ex_name": exercise_name})

    elif exercise_name == 'backward lunges':
        return render(request,'exercises/exercise_backward_lunges.html', {"ex_name": exercise_name})

    else:
        return render(request,'exercises/exercise_cobra_stretch.html', {"ex_name": exercise_name})

def gen(camera):
    
    while True:
        frame = camera.get_frame()
   
        ret, frame = cv2.imencode('.jpg', frame)
        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

def video_feed(request, exercise_name):
    #print(exercise_name)

    time.sleep(1)

    return StreamingHttpResponse(gen(VideoCamera(exercise_name)),
                    content_type='multipart/x-mixed-replace; boundary=frame')

def start_exercise(request, exercise_name):
    
    return render(request, 'exercises/exercise.html', {"ex_name": exercise_name})

def update_Playlist(user_mail, exercise_name):
    
    try:
        playlist = Playlist_Check.objects.get(user_email = user_mail)
    except:
        playlist = Playlist_Check(user_email = user_mail)

    if exercise_name == 'squat':
        playlist.exercise_squats = 1
        playlist.current_date = datetime.date.today()
        playlist.save()

    elif exercise_name == 'jumping jack':
        playlist.exercise_jj = 1
        playlist.current_date = datetime.date.today()
        playlist.save()

    elif exercise_name == 'adbominal crunches':
        playlist.exercise_ac=1
        playlist.current_date = datetime.date.today()
        playlist.save()

    elif exercise_name == 'knee pushup':
        playlist.exercise_kp=1
        playlist.current_date = datetime.date.today()
        playlist.save()
    
    elif exercise_name == 'side arm raises':
        playlist.exercise_sar=1
        playlist.current_date = datetime.date.today()
        playlist.save()

    elif exercise_name == 'backward lunges':
        playlist.exercise_bl=1
        playlist.current_date = datetime.date.today()
        playlist.save()

    else:
        playlist.exercise_cs=1
        playlist.current_date = datetime.date.today()
        playlist.save()

    return(playlist)

def end_workout(request, exercise_name):

    print(exercise_name)

    ex_left = []

    file = open('website/exercise_timing.json', 'r+')

    playlist = update_Playlist(request.session['user_mail_id'], exercise_name)

    if playlist.exercise_jj == 0:
        ex_left.append('jumping jack')
    
    if playlist.exercise_ac == 0:
        ex_left.append('adbominal crunches')
    
    if playlist.exercise_kp == 0:
        ex_left.append('knee pushup')
    
    if playlist.exercise_sar == 0:
        ex_left.append('side arm raises')
    
    if playlist.exercise_squats == 0:
        ex_left.append('squat')
    
    if playlist.exercise_bl == 0:
        ex_left.append('backward lunges')
    
    if playlist.exercise_cs == 0:
        ex_left.append('cobra stretch')

    print(ex_left)

    
    data = json.load(file)

    user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()

    calories, weight_loss = CalorieBurned(data['Total_seconds'], exercise_name, user_data.user_weight).calculate()

    make_exercise_entry = User_Exercise_Info(user_name = user_data.user_name,
                                            exercise_name = exercise_name,
                                            exercise_count = data['Total_Reps'],
                                            exercise_duration = data['Total_seconds'],
                                            exercise_calorie_burnt = calories,
                                            exercise_weight_loss = weight_loss,
                                            current_time = datetime.datetime.now()
                                            )
    
    make_exercise_entry.save()

    file.close()

    return render(request,'exercises/end-workout.html',{"ex_name": exercise_name, 
                                                        "duration": data['Timestamp'][3:],
                                                        "reps": data['Total_Reps'],
                                                        "cal_burned": calories,
                                                        "len_next_ex": len(ex_left),
                                                        "next_exercise": ex_left})

def beginner_playlist(request):

    user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()
    
    return render(request,'beginner.html', {'user_data': user_data})

def profile(request):
    
    user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()

    return render(request,'profile.html',{'user_data': user_data, 'editable': 'False'})

def profile_change(request, editable):

    user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()

    if request.method == 'POST':

        if editable == 'True':
            return render(request,'profile.html',{'user_data': user_data, 'editable': 'True'})

        else:
            user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()

            if request.POST['age'] == '':
                u_age = user_data.user_age
            else:
                u_age = request.POST['age']
                
            if request.POST['weight'] == '':
                u_weight = user_data.user_weight
            else:
                u_weight = request.POST['weight']

            if request.POST['height'] == '':
                u_height = user_data.user_height
            else:
                u_height = request.POST['height']
         
            user_data.user_age = u_age
            user_data.user_weight = u_weight
            user_data.user_height = u_height
            user_data.save()

            user_data = User_Info.objects.filter(user_email=request.session['user_mail_id']).first()

            return render(request,'profile.html',{'user_data': user_data, 'editable': 'False'})

    return render(request,'profile.html',{'user_data': user_data})

