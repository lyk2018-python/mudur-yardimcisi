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
    get_start_time = Profile.objects.get()
    time_now = strftime("%H:%M", gmtime())
    import pdb
    pdb.set_trace()
    get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id
    get_check_id = Check.objects.get_or_create(course_id = get_course_id,user_id=request.user,course_check="")
    get_check_id.save()
    return render(request, 'check_stundent.html',)