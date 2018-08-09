from django.shortcuts import render, redirect, reverse
from django_otp.oath import hotp
from .models import Courses, Profile, Check, Site
from muduryardimci.forms import AuthTokenForm, AddNoteForm
import random
from time import localtime, strftime

def generate_token(request):
    key = bytes(random.randint(1000000, 99999999))
    for i in range(1):
        token = hotp(key=key, counter=i, digits=6)
        if len(str(token)) < 6:
            token = (6 - len(str(token))) * str(random.randint(1, 9)) + str(token)
    get_course_id = Profile.objects.get(user=request.user, is_trainer=True).course_id
    get_course_token = Courses.objects.filter(course_name=get_course_id).update(course_token=token)
    return render(request, 'auth.html', {"token": token})

def stundent_check(request):
    main_site_name = "2018 kamp"
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
    timeout = 20
    if time_now > morning and time_now < afternoon and time_now < evening:
        if time_now > morning + timeout:
            check_time = "Timeout"
        else:
            check_time = "morning"
    elif time_now > morning and time_now > afternoon and time_now < evening:
        if time_now > afternoon + timeout:
            check_time = "Timeout"
        else:
            check_time = "afternoon"
    elif time_now > morning and time_now > afternoon and time_now > evening:
        if time_now > evening + timeout:
            check_time = "timeout"
        else:
            check_time = "evening"

    get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id
    Check.objects.get_or_create(course_id = get_course_id,user_id=request.user)
    if check_time == "evening":
        Check.objects.filter(course_id=get_course_id,user_id=request.user).update(check_evening=True)
        return render(request, 'check_stundent.html',)
    elif check_time == "afternoon":
        Check.objects.filter(course_id=get_course_id, user_id=request.user).update(check_afternoon=True)
        return render(request, 'check_stundent.html',)
    elif check_time == "morning":
        Check.objects.filter(course_id=get_course_id, user_id=request.user).update(check_morning=True)
        return render(request, 'check_stundent.html',)
    elif check_time == "Timeout":
        return("timeout")

def dashboard(request):
    check = Check.objects.all()
    return render(request, 'accounts/dashboard.html', {"check": check})

def AuthToken(request):
    form = AuthTokenForm()
    if request.method == "POST":
        form = AuthTokenForm(request.POST)
        if form.is_valid():
            get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id
            get_course_token = Courses.objects.get(course_name=get_course_id).course_token
            if form.cleaned_data['token_label'] == get_course_token:
                a = stundent_check(request)
                print(type(a))
                import pdb
                pdb.set_trace()
                if type(a) == "'django.http.response.HttpResponse'":
                   print("adadsadsadsadsad")

                else:
                    return redirect(reverse("login"))
                return redirect(reverse("SucsessAuth"))
            else:
                return render(request, "whutt")
    return render(request, 'authlogin.html', {'form' : form})

def SucssesAuth(request):
    return render(request, 'sucssesauth.html')

def AddNote(request):

    def get_form_kwargs(self):
        kwargs = super(AddNote, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    
    get_course_id = Profile.objects.get(user=request.user, is_trainer=False).course_id
    form = AddNoteForm()
    if request.method == "POST":
        form = AddNoteForm(request.POST)
        if form.is_valid():
            get_user = form.cleaned_data['User']
            get_note = form.cleaned_data['Note']
    return render(request, "Addnote.html", {'form' : form})