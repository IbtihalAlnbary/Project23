from django.contrib import admin
# from .models import AddReport, AssignedReport, Workerlogin,citezinreports,ManagerReports
from django.utils import timezone 
from .models import Workerlogin
from django.utils import timezone

# Register your models here.
@admin.register(Workerlogin)
class WorkerloginAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')
