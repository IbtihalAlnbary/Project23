from django.shortcuts import render

from telnetlib import LOGOUT
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password  # Import make_password for password hashing
from django.contrib import messages
# from .models import AddReport
# from .models import AssignedReport 
from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db import transaction
from .models import Workerlogin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from.Form import AddReportForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
# from .models import ManagerReports
# from .models import citezinreports
from .models import Workerlogin
# from .models import AssignedReport
from django.shortcuts import render, get_object_or_404
# from .models import AddReport
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
            return redirect('HomeClient')
            
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
def HomeClient(request):
    return render(request,"mytown/HomeClient.html" )


# from mytown.Form import AddReportForm
def workerlogin(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Hash the password securely
        hashed_password = make_password(password)
        
        # Save the user using your custom Workerlogin model
        Workerlogin.objects.create(
            username=username,
            password=hashed_password,
        )
        return redirect('reports_list')

    return render(request, "mytown/workerlogin.html")

# def workers_list(request):
#     worker = Workerlogin.objects.all()
#     total_reports = Workerlogin.objects.count()
#     return render(request, 'account/workerslist.html', {'worker': worker})

def addreports(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        neighborhood = request.POST.get('neighborhood', '')
        description = request.POST.get('description', '')
        location = request.POST.get('location', '')
        photo = request.FILES.get('photo', None)

        if photo:
            report = AddReport.objects.create(
                title=title,
                neighborhood=neighborhood,
                description=description,
                location=location,
                picture=photo
            )
        else:
            report = AddReport.objects.create(
                title=title,
                neighborhood=neighborhood,
                description=description,
                location=location,
            )
        return redirect('citezinreports')
    else:
        # Handle GET request
        return render(request, 'mytown/addreports.html')
    


def reports_list(request):
    reports = AddReport.objects.all()
    total_reports = AddReport.objects.count()
    choose = request.POST.get('choose', '') == 'on'

    return render(request, 'mytown/reportslist.html', {'reports': reports})

def citizenreports(request):
 reports = AddReport.objects.all()
 total_reports = AddReport.objects.count()
 return render(request, 'mytown/citizenreports.html', {'reports': reports})

def delete(requst,id):
   dele= AddReport.objects.get(pk=id)
   dele.delete()
   return redirect('citezinreports')
   return render(request, 'mytown/citizenreports.html', {'dele': dele})



def managerreports(request):
 reports = AddReport.objects.all()
 total_reports = AddReport.objects.count()
 return render(request, 'mytown/managerlist.html', {'reports': reports})



def updatereport(request, id):
    report = get_object_or_404(AddReport, id=id)
    if request.method == 'POST':
        form = AddReportForm(data=request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('citezinreports')             
    else:
        form = AddReportForm(instance=report)
    return render(request, 'mytown/editreport.html', {'form':form})
        


