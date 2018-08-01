from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

def home(request):
    return redirecet('account/login.html')

def profile(request):
    return redirect('account/profile.html')
