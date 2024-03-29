
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
   
 path('',views.home,name="home"),
 path('signup/',views.signup,name="signup"),
 path('signin/',views.signin,name="signin"),
 path('signout/',views.signout,name="signout"),
 path('homepage/',views.homepage,name="homepage"),
  path('citizenHomepage/',views.citizenHomePage,name="citizenHomepage")


]