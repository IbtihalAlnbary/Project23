from django.shortcuts import render
from telnetlib import LOGOUT
LOGOUT = b'logout'
from django.http import HttpResponse
from .Form import MessageForm

from django.contrib.auth.hashers import make_password  # Import make_password for password hashing
from django.db.models import F

from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from.Form import AddReportForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import ManagerReports
from .models import citezinreports
from .models import Workerlogin
from .models import ContactUs  # Assuming you have a model named ContactUs

# 
from django.shortcuts import render, get_object_or_404
from .models import AddReport

# Create your views here.



def home(request):
    return render(request,"mytown/HomePage.html" )

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



from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        # Check if the entered credentials match the manager's credentials
        if username == 'admin1' and pass1 == '12345':
            # Directly log in the manager
            user = User.objects.get(username='admin1')
            login(request, user)
            return redirect('managerHomePage')
        
        # If not manager's credentials, proceed with normal authentication
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            # Redirect to the client's homepage
            return redirect('HomeClient')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    return render(request, "mytown/signin.html")

def logout_request(request):
    response = LOGOUT  # Assign the logout variable to response
    messages.info(request, "Logged out successfully!")
    return redirect("HomePage")
# def logout_request(request):
#     logout(request)
#     messages.info(request, "Logged out successfully!")
#     return redirect("signin")




def HomePage(request):
    return render(request,"mytown/HomePage.html" )
def HomeClient(request):
    return render(request,"mytown/HomeClient.html" )
def managerHomePage(request):
    return render(request,"mytown/managerHomePage.html" )

def managerSignIn(request):
    return render(request,"mytown/managerSignIn.html" )
def workerHomePage(request):
    return render(request,"mytown/workerHomePage.html" )

def index(request):
    return render(request,"mytown/index.html" )
def home1 (request):
     return render(request, 'mytown/home.html')


def home(request):
    return render(request,"mytown/HomePage.html" )

def loginform (request):
     return render(request, 'mytown/3buttons.html')



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

    return render(request, 'mytown/workerlogin.html')

# def workers_list(request):
#     worker = Workerlogin.objects.all()g
#     total_reports = Workerlogin.objects.count()
#     return render(request, 'account/workerslist.html', {'worker': worker})

def addreports(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        neighborhood = request.POST.get('neighborhood', '')
        facility = request.POST.get('facility', '')  # Corrected field name to lowercase 'facility'
        description = request.POST.get('description', '')
        location = request.POST.get('location', '')
        photo = request.FILES.get('photo', None)

        if photo:
            report = AddReport.objects.create(
                title=title,
                neighborhood=neighborhood,
                facility =facility,
                description=description,
                location=location,
                picture=photo
            )
        else:
            report = AddReport.objects.create(
                title=title,
                neighborhood=neighborhood,
                facility =facility,
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
    choose = request.POST.getlist("boxes")
    for x in choose:
        reports.objects.filter(pk=int(x)).update(choose=True)

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


# def profile(request):
#  profile = signup.objects.all()
# #  total_reports = AddReport.objects.count()
#  return render(request, 'mytown/profile.html', {'profile': profile})

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

def contactus(request):
    if request.method == "POST":
        contact_form = ContactUs()  # Rename the variable
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')  # Fix the variable name
        contact_form.name = name
        contact_form.email = email
        contact_form.description = description
        contact_form.save()
        return HttpResponse("<h1> THANKS FOR CONTACT US</h1>")
    return render(request, 'mytown/contactus.html')
def managermessageworker(request):
    if request.method=="POST":
        messageworker=messageworker()
        name=request.POST.get('name')
        message=request.POST.get('message')
        messageworker.name=name
        messageworker.message=message
        messageworker.save()
        return HttpResponse("<h1> THANK YOU FOR YOUR MESSAGE</h1>")
    return render(request,'mytown/managermessageworker.html')

def managerHomePage(request):
    return render(request,'managerHomePage.html')

def Deletecitizen(request):
    return render(request,'Deletecitizen.html')

def deleteworker(request):
    return render(request,'mytown/deleteworker.html')

def workermessagemanager(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomeClient')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/workermessagemanager.html', {'form': form})


def workerFinish(request):
    return render(request,'workerFinish.html')

        
def managermessagecitizen (request):
    return render(request,'mytown/managermessagecitizen.html')

def citizenmessageworker(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomeClient')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/citizenmessageworker.html', {'form': form})

def workermessagecitizen(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomeClient')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/workermessagecitizen.html', {'form': form})


def managermessageworker(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('HomeClient')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/managermessageworker.html', {'form': form})

