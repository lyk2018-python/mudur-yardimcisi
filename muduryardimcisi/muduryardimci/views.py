from django.shortcuts import render
from django_otp.oath import hotp
from .models import Courses,Profile,Check,Site
import random
from time import gmtime, strftime

def generate_token(request):
    key = bytes(random.randint(1000000,99999999))
    for i in range(1):
        token = hotp(key=key, counter=i, digits=6)
        if len(str(token)) < 6:
            token = (6 - len(str(token))) * str(random.randint(1, 9)) + str(token)
    get_course_id = Profile.objects.get(user=request.user,is_trainer=True).course_id
    get_course_token = Courses.objects.filter(course_name=get_course_id).update(course_token=token)
    return render(request, 'auth.html', {"token": token})

def stundent_check(request):
    main_site_name = "2018 kamp"
    get_start_time = Site.objects.get(is_active=True,name=main_site_name).course_start
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
        number_dec = int(str(find_time - int(find_time))[2:])
        number_dec = (number_dec / 10)
        find_hour = find_time - number_dec
        number_dec = number_dec *60
        find_start_min = int(start_min) + number_dec
        if find_start_min >= 60.0:
            find_start_min -= 60
            find_hour += 1
        return(find_hour,find_start_min)

    print(str(calucate_time("afternoon")))
    hour_now, min_now = str(strftime("%H:%M", gmtime())).split(":")
    #get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id)
    #get_check_id = Check.objects.get_or_create(course_id = get_course_id,user_id=request.user,course_check="")
    #get_check_id.save()
    return render(request, 'check_stundent.html',)
"""
isimler = ["veli","ali","ali","veli","konferans"]

veli: 2
ali:2
konferans:1
"""