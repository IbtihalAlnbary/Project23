from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db import models


class AddReport(models.Model):
    title = models.CharField(max_length=500)

    CITY_CHOICES = [
        ('El-Finesh', 'El-Finesh'),
        ('El-Ubeid', 'El-Ubeid'),
        ('zone 8', 'zone 8'),
        ('zone 3', 'zone 3'),
        ('zone 5', 'zone 5'),
        ('ElQussasi', 'ElQussasi'),
        ('Abu jafar', 'Abu jafar'),
        ('zone 6', 'zone 6'),
        ('Abu Hani', 'Abu Hani'),
        ('El Ubra','El Ubra'),  
        ('El jalawi', 'El jalawi'),
        ('El Qrinawi', 'El Qrinawi'),  
        ('zone 4', 'zone 4'),  
        ('El katnani', 'El katnani'),  
        ('Abu bilal', 'Abu bilal'),  
        ('29', '29'),
        ('27','27'),
        ('21','21'),
         ('25', '25'),  
         ('12', '12'),  
         ('23', '23'),  
         ('15', '15'),  
         ('19', '19'),  

    ]

    

    neighborhood = models.CharField(max_length=15, choices=CITY_CHOICES)
    CHOICES = [
        ('Healthcare Deficiency', 'Healthcare Deficiency'),
        ('Transportation Weakness', 'Transportation Weakness'),
        ('Electricity Service Center', 'Electricity Service Center'),
        ('Water Treatment Plant', 'Water Treatment Plant'),
        ('Road Maintenance Workshop', 'Road Maintenance Workshop'),
        ('Street Lighting Facility', 'Street Lighting Facility'),
        ('Environmental Conservation Hub', 'Environmental Conservation Hub'),
        ('Animal Control Facility', 'Animal Control Facility'),
        ('Traffic',"Traffic"),
        ('other',"other"),


    ]

    facility =models.CharField(max_length=150, choices=CHOICES,default='')
    description = models.CharField(max_length=1000, null=True)
    location = models.CharField(max_length=500)
    picture= models.ImageField(upload_to='images/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
       super().save(*args, **kwargs)  # Call the parent class's save method

         # Create related objects after saving AddReport
       assigned_report = AssignedReport.objects.create(
            choose=False,
            reports=self,  # Use self.id after saving
            reportnumber=self.id,
        )
       manager = ManagerReports.objects.create(
            reports=self,  # Use self.id after saving
            reportnumber=self.id,
        )
       citizen = citezinreports.objects.create(
            reports=self,  # Use self.id after saving
            reportnumber=self.id,
        )
    class Meta:
        db_table = 'addreport'

    def __str__(self):
     return self.title



class AssignedReport(models.Model):
    choose= models.BooleanField('choose',default=False)
    reports = models.ForeignKey(AddReport, blank=True, null=True, on_delete=models.CASCADE)
    reportnumber = models.IntegerField()

    def __str__(self):
        return f"Assigned Report for {self.reports.title}"


class Workerlogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

   
    
    def __str__(self):
        return self.username

   
class Meta:
        db_table = 'workerlogin'

class citezinreports(models.Model):
     reports = models.ForeignKey(AddReport, blank=True, null=True, on_delete=models.CASCADE)
     reportnumber = models.IntegerField(default=0)

def __str__(self):
        return f"Citizen Report for {self.reports.title}"
class Meta:
        db_table = 'citizenreports'



class ManagerReports(models.Model):
    reports = models.ForeignKey(AddReport, blank=True, null=True, on_delete=models.CASCADE)
    reportnumber = models.IntegerField()

    def __str__(self):
        return f"Manager Report for {self.reports.title}"
    class Meta:
        db_table = 'managerreports'


class Message(models.Model):
    worker_name = models.CharField(max_length=255)
    worker_email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Optionally, to record the time of creation

    def __str__(self):
        return f"Message to {self.worker_name} - {self.worker_email}"
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"
    
class workermessagemanager(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from Worker to Manager - {self.created_at}"


class workermessagecitizen(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from Worker to Citizen - {self.created_at}"  
# class contactus(models.Model):
#     worker_name = models.CharField(max_length=255)
#     worker_email = models.EmailField()
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)  # Optionally, to record the time of creation

#     def __str__(self):
#         return f"Message to {self.worker_name} - {self.worker_email}"
# class workerslist(models.Model):
#     workers = models.OneToOneField(Workerlogin, on_delete=models.CASCADE)
#     number = models.IntegerField(default=0)

    
#     def __str__(self):
#         return f"Report for {self.workers.username}"

#     class Meta:
#         db_table = 'workerslist'

# class Ckeckreport(models.Model):
#     reports = models.ForeignKey(AddReport, blank=True, null=True, on_delete=models.CASCADE)
#     choose = models.BooleanField(default=False)  
#     def __str__(self):
#         return f"Check Report for {self.reports.title}"