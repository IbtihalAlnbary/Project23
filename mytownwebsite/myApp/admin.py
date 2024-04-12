from django.contrib import admin
from .models import AddReport
from .models import AddReport, AssignedReport, Workerlogin, ManagerReports, Message, ContactUs,workermessagemanager,workermessagecitizen
from django.utils import timezone 
from .models import citizenReports
from django.utils import timezone
@admin.register(AddReport)
class AddReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'neighborhood', 'facility','description', 'location', 'picture')

@admin.register(AssignedReport)
class AssignedReportAdmin(admin.ModelAdmin):
    list_display = ( 'choose', 'reports', 'reportnumber')
    list_filter = ('choose','reportnumber')
    search_fields = ('reports__title', 'reports__description')

@admin.register(Workerlogin)
class WorkerloginAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


@admin.register(ManagerReports)
class ManagerReporstAdmin(admin.ModelAdmin):
    list_display = ('reports', 'reportnumber')
    list_filter = ('reportnumber','reports')
    search_fields = ('reports__title','reports__description')

@admin.register(citizenReports)
class CitezinReportAdmin(admin.ModelAdmin):
    list_display = ( 'reports', 'reportnumber')
    list_filter = ('reportnumber',)  # Update this line to reference existing fields
    search_fields = ('reports__title', 'reports__description')
# @admin.register(Workerslist)
# class WorkerslistAdmin(admin.ModelAdmin):
#     list_display = ('number','worker')
#     list_filter = ('id','number')
#     search_fields=('id','number')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('worker_name', 'worker_email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('worker_name', 'message')

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')

@admin.register(workermessagemanager)
class workermessagemanagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')

@admin.register(workermessagecitizen)
class workermessagecitizenAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')