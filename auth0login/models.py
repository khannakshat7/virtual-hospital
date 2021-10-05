from django.db import models

# Create your models here.

# Model to store appointments
class appointment(models.Model):
    appointmentid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    doctorName = models.CharField(max_length=100)
    prevReport = models.FileField(upload_to='uploadsReport/')
    prevScans = models.FileField(upload_to='uploadsScans/')
    status = models.BooleanField(default=False)
    medicines = models.CharField(max_length=250,blank=True)
    tests = models.CharField(max_length=250,blank=True)
    summery = models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doctorName
