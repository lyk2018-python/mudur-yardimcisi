from django.shortcuts import render, redirect, reverse
from django_otp.oath import hotp
from django.http import HttpResponse,HttpResponseRedirect
from .models import Courses, Profile, Check, Site
from muduryardimci.forms import AuthTokenForm
from django.utils import timezone
import random
from time import localtime, strftime

def superuser_token(request):
    hour_now, min_now = str(strftime("%H:%M", localtime())).split(":")
    course_list = []
    get_course_id = Profile.objects.get(user=request.user)
    all_courses = Courses.objects.all()
    for i in all_courses:
        key = bytes(random.randint(1000000, 99999999))
        for k in range(1):
            token = hotp(key=key, counter=k, digits=6)
            if len(str(token)) < 10:
                token = (10 - len(str(token))) * str(random.randint(1, 9)) + str(token)
        course_list +=([i.course_name,i.course_token,token])
        #print(course_list[0:1])
        token_cache = int(token)
    if get_course_id.is_trainer == True:
        print("")
        get_course_id = get_course_id.course_id
    else:
        token = "ACCESS DENIED"
    if request.user.is_superuser == True:
        print("")
        token = int(token_cache)
        token = str(token) + str(hour_now) +str(min_now)
    get_course_token = Courses.objects.filter(course_name=get_course_id).update(course_token=token)
    if request.user.is_superuser == True:
        get_course_token = Courses.objects.all().update(course_token=token)
    return render(request, 'auth.html', {"token": token})


def generate_token(request):
    hour_now, min_now = str(strftime("%H:%M", localtime())).split(":")
    key = bytes(random.randint(1000000, 99999999))
    for i in range(1):
        token = hotp(key=key, counter=i, digits=6)
        token = str(token) + str(hour_now) + str(min_now)
        if len(str(token)) < 10:
            token = (10 - len(str(token))) * str(random.randint(1, 9)) + str(token)
    get_course_id = Profile.objects.get(user=request.user)
    if get_course_id.is_trainer == True:
        print("")
        get_course_id = get_course_id.course_id
    else:
        token = "ACCESS DENIED"
    get_course_token = Courses.objects.filter(course_name=get_course_id).update(course_token=token)
    return render(request, 'auth.html', {"token": token})

def stundent_check(request):
    main_site_name = Site.objects.get(is_active=True).name
    get_start_time = Site.objects.get(is_active=True, name=main_site_name).course_start
    get_total_morning_date = float(Site.objects.get(is_active=True, name=main_site_name).total_morning_date)
    get_total_afternoon_date = float(Site.objects.get(is_active=True, name=main_site_name).total_afternoon_date)
    def calucate_time(time):
        try:
            start_hour, start_min = str(get_start_time).split(":")
        except TypeError:
            return ("Fatal Error... ")
        if time == "evening":
            find_time = int(start_hour) + get_total_morning_date + get_total_afternoon_date
        elif time == "afternoon":
            find_time = int(start_hour) + get_total_morning_date
        elif time == "morning":
            find_time = float(start_hour)
        number_dec = int(str(find_time - int(find_time))[2:])
        number_dec = (number_dec / 10)
        find_hour = find_time - number_dec
        number_dec = number_dec *60
        find_start_min = int(start_min) + number_dec
        if find_start_min >= 60.0:
            find_start_min -= 60
            find_hour += 1
        start_min = float(find_start_min) / 100.0
        find_time = float(find_hour) + start_min
        return(find_time)
    afternoon = calucate_time("afternoon")
    evening = calucate_time("evening")
    morning = calucate_time("morning")
    hour_now, min_now = str(strftime("%H:%M", localtime())).split(":")
    min_now = float(min_now) /100
    hour_now = float(hour_now)
    time_now = hour_now + min_now
    timeout = 0.2 ## 20 min
    #print(time_now,morning,afternoon,evening) ## Some Print Debugging :) Yep ı dont love logging libary
    if time_now >= morning and time_now < afternoon and time_now < evening:
        if time_now > morning + timeout:
            check_time = "Timeout"
        else:
            check_time = "morning"
    elif time_now > morning and time_now >= afternoon and time_now < evening:
        if time_now > afternoon + timeout:
            check_time = "Timeout"
        else:
            check_time = "afternoon"
    elif time_now > morning and time_now > afternoon and time_now >= evening:
        if time_now > evening + timeout:
            check_time = "Timeout"
        else:
            check_time = "evening"
    #print(check_time)
    get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id
    Check.objects.get_or_create(course_id = get_course_id,user_id=request.user,check_date=timezone.now())
    if check_time == "Timeout":
        return "timeout"
    elif check_time == "evening":
        Check.objects.filter(course_id=get_course_id,user_id=request.user).update(check_evening=True)
        return render(request, 'check_stundent.html',)
    elif check_time == "afternoon":
        Check.objects.filter(course_id=get_course_id, user_id=request.user).update(check_afternoon=True)
        return render(request, 'check_stundent.html',)
    elif check_time == "morning":
        Check.objects.filter(course_id=get_course_id, user_id=request.user).update(check_morning=True)
        return render(request, 'check_stundent.html',)
def dashboard(request):
    course_id = Profile.objects.get(user=request.user).course_id
    check = Check.objects.filter(course_id=course_id,check_date=timezone.now())
    try :
        is_trainer = Profile.objects.get(user=request.user)
    except TypeError:
        return render(request, 'err.html')
    return render(request, 'accounts/dashboard.html', {"check": check, "profile" : is_trainer})

def AuthToken(request):
    get_token_remains = Profile.objects.get(user=request.user).token_remains
    if int(get_token_remains) <= 0:
        banned = True
        return HttpResponse("<html><strong>Your account has been disabled. Contact your trainer</strong></html>")
    form = AuthTokenForm()
    if request.method == "POST":
        form = AuthTokenForm(request.POST)
        if form.is_valid():
            get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id
            get_course_token = Courses.objects.get(course_name=get_course_id).course_token
            hour_now, min_now = str(strftime("%H:%M", localtime())).split(":")
            min_now = float(min_now) / 100
            hour_now = float(hour_now)
            time_now = hour_now + min_now
            token_label = form.cleaned_data['token_label']
            token_hour = int(token_label[6:8])
            token_min = int(token_label[8:]) / 100
            time_token = token_hour + token_min ## Calucating token time.
            if token_label == get_course_token and (time_now - time_token) <= 0.6:
                a = stundent_check(request)
                if a == "timeout":
                    return HttpResponse("<html><strong>I am Sorry Dude Timeout.</strong></html>")
                else:
                    return HttpResponse("<html><strong>Thanks For Checking. :)</strong></html>")
                update_token_remains = Profile.objects.filter(user=request.user).update(token_remains=3)

            else:
                Profile.objects.filter(user=request.user).update(token_remains=get_token_remains - 1)
                return HttpResponse("<strong><p>Token Error.</strong></html>")
    return render(request, 'authlogin.html', {'form' : form, "token_remains" : get_token_remains,})
