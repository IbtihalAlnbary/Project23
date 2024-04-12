from django.shortcuts import render
from telnetlib import LOGOUT
LOGOUT = b'logout'
from django.http import HttpResponse
from .Form import MessageForm

from django.contrib.auth.hashers import make_password  # Import make_password for password hashing
from django.db.models import F
from django.contrib.auth.hashers import check_password

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
from .models import citizenReports
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

def addWorker(request):
    return render(request,"mytown/addWorker.html" )


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
        
        if username == 'Worker':
            # Directly log in the manager
            user = User.objects.get(username='Worker')
            login(request, user)
            return redirect('reportlists')
        

   
        # Check if the entered credentials match the manager's credentials
        if username == 'admin1' and pass1 == '12345':
            # Directly log in the manager
            user = User.objects.get(username='admin1')
            login(request, user)
            return redirect('managerreports')
        
        # If not manager's credentials, proceed with normal authentication
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            # If authentication is successful, log in the user
            login(request, user)
            # Redirect to the client's homepage
            return redirect('citezinreports')
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')
    return render(request, "mytown/signin.html")

def logout_request(request):
    response = LOGOUT  # Assign the logout variable to response
    messages.info(request, "Logged out successfully!")
    return redirect("home")
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Check if the user is marked as staff
            user = User.objects.filter(username=username, is_staff=True).first()

            if user and user.check_password(password):
                # Check if a worker with the provided username exists
                worker, created = Workerlogin.objects.get_or_create(username=username)

                # Update the worker's password without hashing
                worker.password = password
                worker.save()

                request.session['username'] = username
                messages.success(request, 'Worker details updated successfully')

                return redirect('reports_list')  # Redirect to the reports list page or any other page

            # else:
            #     messages.error(request, 'Invalid username or password')
                
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'mytown/workerlogin.html')


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
                 user=request.user,
                title=title,
                neighborhood=neighborhood,
                facility =facility,
                description=description,
                location=location,
                picture=photo
            )
        else:
            report = AddReport.objects.create(
                 user=request.user,
                title=title,
                neighborhood=neighborhood,
                facility =facility,
                description=description,
                location=location,
            )
            
            # Storing the ID of the created report in the session
        request.session['report_id'] = report.id
        return redirect('citezinreports')
    else:
        # Handle GET request
        return render(request, 'mytown/addreports.html')

def reports_list(request):
    if request.method == 'POST':
        choose = request.POST.getlist("boxes")
        for report_id in choose:
            report = AddReport.objects.get(pk=int(report_id))
            report.assignedreport.choose = True
            report.assignedreport.save()
            # Add logic to notify other workers
    reports = AddReport.objects.all()
    return render(request, 'mytown/reportslist.html', {'reports': reports})


def citizenreports(request):
    user_reports = AddReport.objects.filter(user=request.user)
    return render(request, 'mytown/citizenreports.html', {'user_reports': user_reports})

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
        # return HttpResponse("<h1> THANKS FOR CONTACT US</h1>")
    return render(request, 'mytown/contactus.html')
def managermessageworker(request):
    if request.method=="POST":
        messageworker=messageworker()
        name=request.POST.get('name')
        message=request.POST.get('message')
        messageworker.name=name
        messageworker.message=message
        messageworker.save()
        # return HttpResponse("<h1> THANK YOU FOR YOUR MESSAGE</h1>")
    return render(request,'mytown/managermessageworker.html')

def managermessagecitizen(request):
    if request.method=="POST":
        managermessagecitizen=managermessagecitizen()
        name=request.POST.get('name')
        message=request.POST.get('message')
        managermessagecitizen.name=name
        managermessagecitizen.message=message
        managermessagecitizen.save()
        # return HttpResponse("<h1> THANK YOU FOR YOUR MESSAGE</h1>")
    return render(request,'mytown/managermessagecitizen.html')

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
            return redirect('workermessagemanager')  # Redirect to a new URL
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
            return redirect('citizenmessageworker')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/citizenmessageworker.html', {'form': form})

def workermessagecitizen(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workermessagecitizen')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/workermessagecitizen.html', {'form': form})


def managermessageworker(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managermessageworker')  # Redirect to a new URL
    else:
        form = MessageForm()
    return render(request, 'mytown/managermessageworker.html', {'form': form})

# import unittest
# from django.test import Client
# #from myapp.models import MessageWorker  # אני מניח שיש לך מודל בשם MessageWorker

# class TestManagerMessageWorkerView(unittest.TestCase):
    
#     def test_post_request(self):
#         client = Client()
#         response = client.post('/managermessageworker/', {'name': 'John Doe', 'message': 'Test message'})
#         self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

#         # Check if message is saved in the database
#         self.assertTrue(MessageWorker.objects.filter(name='John Doe', message='Test message').exists())

#     def test_get_request(self):
#         client = Client()
#         response = client.get('/managermessageworker/')
#         self.assertEqual(response.status_code, 200)  # Assuming the view returns a success response

#         # Add more assertions if necessary

# if __name__ == '__main__':
#     unittest.main()

def workermessagemanager(request):
    if request.method=="POST":
        workermessagemanager=workermessagemanager()
        name=request.POST.get('name')
        message=request.POST.get('message')
        workermessagemanager.name=name
        workermessagemanager.message=message
        workermessagemanager.save()
        # return HttpResponse("<h1> THANK YOU FOR YOUR MESSAGE</h1>")
    return render(request,'mytown/workermessagemanager.html')

def workermessagecitizen(request):
    if request.method=="POST":
        workermessagecitizen=workermessagecitizen()
        name=request.POST.get('name')
        message=request.POST.get('message')
        workermessagecitizen.name=name
        workermessagecitizen.message=message
        workermessagecitizen.save()
        return HttpResponse("<h1> THANK YOU FOR YOUR MESSAGE</h1>")
    return render(request,'mytown/workermessagecitizen.html')
from django.shortcuts import render
from django.http import HttpResponse

def delete_worker(request):
    if request.method == "POST":
        # Get data from the form
        worker_name = request.POST.get('workerName')
        worker_id = request.POST.get('workerID')
        reason = request.POST.get('reason')
        
        # Perform deletion logic here (e.g., delete the worker from the database)
        # Example:
        # worker = Worker.objects.get(name=worker_name, id=worker_id)
        # worker.delete()
        
        return HttpResponse("<h1>Worker Deleted Successfully</h1>")
    
    # If the request method is not POST, render the delete worker page
    return render(request, 'mytown/delete_worker.html')

from django.shortcuts import render
from django.http import HttpResponse

def finish_job(request):
    if request.method == "POST":
        # Get data from the form
        work_place = request.POST.get('workPlace')
        work_duration = request.POST.get('workDuration')
        additional_notes = request.POST.get('additionalNotes')
        
        # Perform any additional logic here (e.g., save data to the database)
        
        # Return a response
        return HttpResponse("<h1>Job Finished Successfully</h1>")
    
    # If the request method is not POST, render the finish job page
    return render(request, 'mytown/finish_job.html')
