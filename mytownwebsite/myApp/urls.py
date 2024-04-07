# from django.contrib import admin
# from django.urls import path, include
# from . import views 

# #list of all urls i want add
# urlpatterns = [
#     path("", views.home,name="home")
# ]




from django.urls import path 
from . import views 

#list of all urls i want add
# urlpatterns = [
#  path("citizen/",views.index)
# ]

urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    # path('signout/', views.signout, name="signout"),
    path('HomePage/', views.HomePage, name="HomePage"),
    path('HomeClient/', views.HomeClient, name="HomeClient"),
    path('managerHomePage/', views.managerHomePage, name="managerHomePage"),
    path('managerSignIn/', views.managerSignIn, name="managerSignIn"),
    path('index/', views.index, name="index"),
    path('workerHomePage/', views.workerHomePage, name="workerHomePage"),

    path('citizenHomepage/', views.citizenHomePage, name="citizenHomepage"),
    path('logout/', views.logout_request, name="logout"),

]