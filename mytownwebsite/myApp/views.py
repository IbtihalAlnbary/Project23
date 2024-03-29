from django.shortcuts import render

from telnetlib import LOGOUT
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
# Create your views here.



def home(request):
    return render(request,"mytown/index.html" )

def citizenHomePage(request):
    return render(request,"mytown/citizenHomePage.html" )




def signup(request):
   
    if request.method == "POST":
   
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname  # Corrected the attribute name

            myuser.save()  # Corrected method name

            messages.success(request, "Your account has been successfully created!")
            return redirect('signin')

        else:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

    return render(request, "mytown/signup.html")

def signin(request):

    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']

        user=authenticate(username=username, password=pass1 )
        if user is not None:
            login(request, user)
            fname = user.first_name 
            return render(request,"mytown/index", {'fname':fname})
            
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request,"mytown/signin.html" )

def signout(request):
    LOGOUT(request)
    messages.SUCCESS(request,"logged out successfully!")
    return redirect('home')


def homepage(request):
    return render(request,"homepage" )
