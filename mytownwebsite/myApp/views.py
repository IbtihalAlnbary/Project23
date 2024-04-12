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
from django.db.models import F

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
from.Form import AddReportForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from .models import ManagerReports,AssignedReport
from .models import citezinReports
from .models import Workerlogin
# 
from django.shortcuts import render, get_object_or_404
from .models import AddReport
# Create your views here.

def home1 (request):
     return render(request, 'mytown/home.html')

def loginform (request):
     return render(request, 'mytown/3buttons.html')



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
            report.Assignedreport.choose = True
            report.Assignedreport.save()
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
        


