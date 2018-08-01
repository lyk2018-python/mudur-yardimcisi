from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login



def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...



def home(request):
    return redirecet('account/login.html')

def profile(request):
    return redirect('account/profile.html')
