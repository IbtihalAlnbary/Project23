from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db import models


class Workerlogin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    # def save(self, *args, **kwargs):
    #    super().save(*args, **kwargs)  # Call the parent class's save method
    #    created = not self.pk  # Check if the instance is being created or updated

    #    if created:
    #         # If the Workerlogin instance is new, create a corresponding workerslist entry
    #      workerslist.objects.create(
    #              workers=self,
    #             number=self.id,
    #         )

    
    def __str__(self):
        return self.username

   
class Meta:
        db_table = 'workerlogin'
