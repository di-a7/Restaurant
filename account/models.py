from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import time,date
from django.utils import timezone
from django.db.models import Sum

# Create your models here.

class User(AbstractUser):
	ROLE_CHOICES = (
		('admin','Admin'),
		('manager','Manager'),
		('waiter','Waiter'),
		('chef','Chef'),
		('cashier','Cashier'),
	)
	role = models.CharField(max_length=15,choices=ROLE_CHOICES,null=True,blank=True)

class Staff(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   contact= models.CharField(max_length=10, validators=[
      RegexValidator(regex='^[0-9]{10}$', message=('Contact information must be a 10-digit number.'), code='invalid_contact_information')
   ])
   def __str__(self):
      return self.user.username

class Shift(models.Model):
   SHIFT_CHOICES = [
      ('MORNING', 'Morning'),
      ('DAY', 'Day'),
      ('EVENING', 'Evening'),
   ]
   staff= models.ForeignKey(Staff, on_delete=models.CASCADE,related_name='shifts',null=True,blank=True)
   shift = models.CharField(max_length = 10, choices = SHIFT_CHOICES,default='DAY')
   date = models.DateField(default=timezone.now)
   start_time = models.TimeField(null=True,blank=True)
   end_time = models.TimeField(null=True,blank=True)
   def save(self, *args, **kwargs):
      if self.shift == 'MORNING':
         self.start_time = time(hour=6)
         self.end_time = time(hour=11)
      elif self.shift == 'DAY':
         self.start_time = time(hour=11)
         self.end_time = time(hour=16)
      elif self.shift == 'EVENING':
         self.start_time = time(hour=16)
         self.end_time = time(hour=21)
      super().save(*args, **kwargs)
   def __str__(self):
      return f"{self.shift}-{self.date}"

class TimeOffRequest(models.Model):
   staff = models.ForeignKey(Staff, on_delete=models.CASCADE,null=True, blank=True)
   STATUS_CHOICES = [
      ('PENDING', 'Pending'),
      ('APPROVED', 'Approved'),
      ('DECLINED', 'Declined'),
   ]
   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
   date_from = models.DateField(default=date.today)
   date_to = models.DateField(default=date.today)
   comments = models.TextField(max_length=250, blank=True,null=True)
   
   def __str__(self) -> str:
      return f"{self.staff}"

# class ShaffLog(models.Model):
#    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#    shift = models.Foreignkey(Shift, on_delete=models.CASCADE)
#    timeoff = models.ForeignKey(TimeOffRequest, on_delete=models.CASCADE)
   
