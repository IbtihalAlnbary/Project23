from django.shortcuts import render

from telnetlib import LOGOUT
LOGOUT = b'logout'
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
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

# def sign_out(request):
#     LOGOUT(request)
#     return redirect('home')





# def signin(request):
#     if request.method == 'POST':
#         username=request.POST['username']
#         pass1=request.POST['pass1']
#         user=authenticate(username=username, password=pass1 )
#         if user is not None:
#             login(request, user)
#             fname = user.first_name 
#             return redirect('HomeClient')
            
#         else:
#             messages.error(request, "Bad Credentials!")
#             return redirect('home')
#     return render(request,"mytown/signin.html" )
