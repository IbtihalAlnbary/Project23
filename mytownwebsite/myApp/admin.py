from django.contrib import admin
from .models import AddReport
from .models import AddReport, AssignedReport, Workerlogin,citezinReports,ManagerReports
from django.utils import timezone 

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

@admin.register(citezinReports)
class CitezinReportAdmin(admin.ModelAdmin):
    list_display = ( 'reports', 'reportnumber')
    list_filter = ('reportnumber',)  # Update this line to reference existing fields
    search_fields = ('reports__title', 'reports__description')
# @admin.register(Workerslist)
# class WorkerslistAdmin(admin.ModelAdmin):
#     list_display = ('number','worker')
#     list_filter = ('id','number')
#     search_fields=('id','number')