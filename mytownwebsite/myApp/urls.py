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
     path('workerlogin/', views.workerlogin,name="workerlogin"),
    path('addreports/', views.addreports,name="addreports"),
    path('reportslist/', views.reports_list, name='reports_list'),
    path('citezenreports/', views.citizenreports, name='citezinreports'),
    path('managerreports/', views.managerreports, name='managerreports'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('updatereport/<int:id>/', views.updatereport, name='updatereport'),
    # path('Reports/', views.check_reports, name='ckeck_reports'),
     path('', views.home1, name='home'),
    path('loginform/', views.loginform, name='loginform'),
]