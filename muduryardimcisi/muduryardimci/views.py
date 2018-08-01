from django.shortcuts import render
from django_otp.oath import hotp
from .models import Courses,Profile
import random
def generate_token(request):
    key = bytes(random.randint(1000000,99999999))
    for i in range(1):
        token = hotp(key=key, counter=i, digits=6)
        if len(str(token)) < 6:
            token = (6 - len(str(token))) * str(random.randint(1, 9)) + str(token)
    get_course_id = Profile.objects.get(user=request.user).course_id
    get_course_token = Courses.objects.get(course_name=get_course_id)
    get_course_token.course_token = token

    return render(request, 'auth.html', {"token": token})