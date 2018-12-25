from django.shortcuts import render, redirect

def home(request):
    return redirect('/login')

def profile(request):
    return redirect('accounts')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def support(request):
    return render(request, 'support.html')
